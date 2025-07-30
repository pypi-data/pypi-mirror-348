# 🌐 `@geo watch`

watch the planet's story unfold: [targets](./targets.geojson).


```bash
@geo watch help
```
<details>
<summary></summary>

help::: bluer_geo watch

</details>

## example run

```bash
@select geo-watch-$(@@timestamp)
@geo watch - \
  target=Miduk-test - \
  to=local - - .
@assets publish \
	extensions=png+gif,push .
```

set:::object_name geo-watch-2025-05-17-20-53-04-sti48v

assets:::get:::object_name/get:::object_name.gif

--scale-note--

--table--
