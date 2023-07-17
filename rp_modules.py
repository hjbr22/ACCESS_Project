def get_modules_and_versions(filename,modulesAndVersions={}):
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
        # moduleAndVersion = []
        modules = []
        for mod in mods.split("\n"):
            # Ignore all characters used for separations or descriptions
            if ("----" in mod) or ("/opt" in mod) or ("(L" in mod) or ("D)" in mod):
                pass
            else:
                if "/" in mod:
                    moduleName, moduleVersion = mod.split("/", 1)
                    moduleName = moduleName.strip()
                    if moduleName not in modules:
                        modules.append(moduleName)
                    if (moduleName in modulesAndVersions) and (moduleVersion not in modulesAndVersions[moduleName]):
                        modulesAndVersions[moduleName] += f", {moduleVersion}"
                    else:
                        modulesAndVersions[moduleName] = moduleVersion
                else:
                    # If the app has no version
                    if mod not in modules:
                        modules.append(mod)
                    if (mod not in modulesAndVersions):
                        modulesAndVersions[mod] = ''
    return(modulesAndVersions, modules)
