-- Pandoc-filter: zet LaTeX-omgevingen om naar Word-stijlen.
-- Gebruik: pandoc ... --lua-filter=filter.lua -M versie=leerling|docent

local stijlen = {
  theorie="Theorie", voorbeeld="Voorbeeld", letop="LetOp", doel="Doel", ict="ICT",
  oplossing="Oplossing", missie="Missie", titel="Voorblad Titel", ondertitel="Voorblad Subtitel",
  banner="Banner", midden="Midden",
}
local docent = false

local function stijl(el)
  for _,c in ipairs(el.classes) do
    if stijlen[c] then return stijlen[c], c end
  end
end

local function heeft_tekst(inl, t)
  return #inl == 1 and inl[1].t == "Str" and inl[1].text == t
end

local function pagina_einde()
  return pandoc.RawBlock("openxml", '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
end

function Pandoc(doc)
  local v = doc.meta.versie
  if v and pandoc.utils.stringify(v) == "docent" then docent = true end

  local nieuw = doc:walk({
    Div = function(el)
      for _, cl in ipairs(el.classes) do
        if cl == "docentenpagina" then
          if not docent then return {} else return el.content end
        end
      end
      local s, c = stijl(el)
      if not s then return nil end
      if c == "oplossing" then
        if not docent then return {} end
      end
      el.attributes["custom-style"] = s
      -- kader = tabel met 1 cel (zodat lijsten en alinea's samen in één kader blijven)
      local kaders = {theorie=1, voorbeeld=1, letop=1, doel=1, ict=1, oplossing=1}
      if kaders[c] then
        local simple = pandoc.SimpleTable({}, {pandoc.AlignLeft}, {0}, {}, {{el.content}})
        local tbl = pandoc.utils.from_simple_table(simple)
        local ruimte = pandoc.RawBlock("openxml", '<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="120" w:lineRule="exact"/></w:pPr></w:p>')
        return {ruimte, pandoc.Div({tbl}, pandoc.Attr("", {c}, {["custom-style"]=s})), ruimte}
      end
      return el
    end,
    Para = function(el)
      if heeft_tekst(el.content, "LIJN") then
        return pandoc.Div({pandoc.Para({pandoc.Str("\u{00A0}")})}, pandoc.Attr("", {}, {["custom-style"]="Antwoordlijn"}))
      end
      if heeft_tekst(el.content, "PAGEBREAK") then return pagina_einde() end
      if #el.content == 1 and el.content[1].t == "Image" then
        return pandoc.Div({el}, pandoc.Attr("", {}, {["custom-style"]="Afbeelding"}))
      end
    end,
    -- \gat{woord}  (\textsc): leerling ziet een invulplaats, docent het antwoord
    SmallCaps = function(el)
      if docent then
        return pandoc.Span(el.content, pandoc.Attr("", {}, {["custom-style"]="OplossingTekst"}))
      else
        return pandoc.Span({pandoc.Str("\u{2026}\u{2026}\u{2026}\u{2026}\u{2026}\u{2026}\u{2026}")}, pandoc.Attr("", {}, {["custom-style"]="Gat"}))
      end
    end,
  })
  -- tweede doorgang: kolombreedtes (\breedtes{20/50/30} vóór een tabel)
  return nieuw:walk({
    Blocks = function(blocks)
      local out = pandoc.List()
      local wachtend = nil
      for _, b in ipairs(blocks) do
        if b.t == "Para" and #b.content == 1 and b.content[1].t == "Str" and b.content[1].text:match("^BREEDTE:") then
          wachtend = {}
          for n in b.content[1].text:gmatch("%d+") do table.insert(wachtend, tonumber(n)) end
        elseif b.t == "Table" and wachtend then
          local totaal = 0
          for _, v in ipairs(wachtend) do totaal = totaal + v end
          for k, cs in ipairs(b.colspecs) do
            if wachtend[k] then cs[2] = wachtend[k] / totaal end
          end
          wachtend = nil
          out:insert(b)
        else
          out:insert(b)
        end
      end
      return out
    end,
  })
end
