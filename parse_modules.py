
def get_modules_and_versions(filename):
    """
    Takes as input a filename or path
    returns a nested list of modules where the first item 
    is the module name and the second is the module version

    The input file must contain the raw output gotten from running
    'module avail &> <file-name>.txt' on an RP
    """
    with open(filename) as rpMods:
        content = rpMods.read()
        # The list of modules will end at 'Where:' so we ignore everything afterwards
        mods = content.split("Where:")[0]
        moduleAndVersion = []
        moduleVRS = {}
        for mod in mods.split():
            # Ignore all characters used for separations or descriptions
            if ("----" in mod) or ("/opt" in mod) or ("(L" in mod) or (",L" in mod) or ("D)" in mod) or ("(c" in mod) or ("(g" in mod) or ("(e" in mod):
                pass
            else:
                if "/" in mod:
                    moduleName, moduleVersion = mod.split("/", 1)
                    if moduleName in moduleVRS:
                        moduleVRS[moduleName] += f", {moduleVersion}"
                    else:
                        moduleVRS[moduleName] = moduleVersion
                else:
                    # If the app has no version
                    moduleVRS[mod] = ''
        moduleAndVersion = [[moduleName, moduleVersion] for moduleName, moduleVersion in moduleVRS.items()]
    return(moduleAndVersion)