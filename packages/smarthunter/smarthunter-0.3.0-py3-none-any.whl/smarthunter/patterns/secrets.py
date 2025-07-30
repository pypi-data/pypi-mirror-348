from ..core import pattern

pattern("Email",3.0)(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

pattern("URL",2.5)(r"\b(?:https?://|www\.)[^\s/$.?#].[^\s]*")

pattern("Secret",4.0)(r"\b(?:token|secret|password|passwd|pwd|apikey|key)=\S+") 