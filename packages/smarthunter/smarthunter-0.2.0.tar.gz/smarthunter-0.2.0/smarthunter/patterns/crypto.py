from ..core import pattern

pattern("BTC",3.5)(r"\b(?:bc1|[13])[A-HJ-NP-Za-km-z1-9]{25,39}\b")

pattern("ETH",3.0)(r"\b0x[a-fA-F0-9]{40}\b") 