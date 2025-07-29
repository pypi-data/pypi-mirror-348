#!/usr/bin/env python3

"""Simple examples for dm-ollamalib"""

from dm_ollamalib.optionhelper import help_long, help_overview, to_ollama_options

print(help_overview())
print(help_long())

print(to_ollama_options("top_p=0.9;temperature=0.8"))
