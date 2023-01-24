import plotly.express as px


orange = '#EA7C5A'  # → orange
mokka = '#645A5A'  # → mokka
yellow = '#FED542'  # → yellow
heather = '#B4A0AA'  # → heather
graphite = '#3C3C4C'  # → graphite
plum = '#965F77'  # → plum
mint = '#6ABA9C'  # → mint
azure = '#7896CF'  # → azure
azure_dark = '#52a2bf'  # → azure

ntg = px.colors.make_colorscale(
    [yellow, mokka, orange, heather, graphite, plum, mint, azure])

ntg_map = px.colors.make_colorscale(
    [graphite, plum, azure_dark, orange, yellow])

ntg_av = px.colors.make_colorscale(
    [graphite, mokka, yellow, orange, plum, heather])


colorscales = px.colors.named_colorscales()
colorscales.append(ntg)
colorscales.append(ntg_map)
colorscales.append(ntg_av)
