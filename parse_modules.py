
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
        for mod in mods.split():
            # Ignore all characters used for separations or descriptions
            if ("----" in mod) or ("/opt" in mod) or ("(L" in mod) or ("D)" in mod):
                pass
            else:
                if "/" in mod:
                    # Separate modules by name and version
                    moduleAndVersion.append(mod.split("/"))
                else:
                    # If the app has no version
                    moduleAndVersion.append([mod,''])
    return(moduleAndVersion)