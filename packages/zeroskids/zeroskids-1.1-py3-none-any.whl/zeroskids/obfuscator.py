def obfuscate(code: str) -> str:
    hexified = ''.join(f'\\x{ord(c):02x}' for c in code)
    watermark = "# ts script has been obfuscated with the python package 'ZeroSkids'!!!!!!!!! omg so cool!!!!! no skids!!!!! try to skid this!!!!!!!\n"
    return watermark + 'exec("' + hexified + '")'
