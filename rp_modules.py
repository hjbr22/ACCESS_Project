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
        # print(mods.split("\n"))
        for mod in mods.split("\n"):
            # Ignore all characters used for separations or descriptions
            if ("----" in mod) or ("/opt" in mod) or ("(L" in mod) or ("D)" in mod):
                pass
            else:
                if "/" in mod:
                    moduleName, moduleVersion = mod.split("/", 1)
                    moduleName = moduleName.strip()
                    if moduleName not in modules:
                        # print("module: ", moduleName)
                        modules.append(moduleName)
                    if (moduleName in modulesAndVersions) and (moduleVersion not in modulesAndVersions[moduleName]):
                        # print("module: ", moduleVersion.strip())
                        if moduleVersion:
                            modulesAndVersions[moduleName] += f",{moduleVersion.strip()}"
                            # print(modulesAndVersions[moduleName])
                    else:
                        modulesAndVersions[moduleName] = moduleVersion.strip()
                else:
                    # print(mod.strip())
                    # If the app has no version
                    if mod not in modules:
                        modules.append(mod.strip())
                    if (mod not in modulesAndVersions):
                        # print(modulesAndVersions)
                        # print(modulesAndVersions.items())
                        modulesAndVersions[mod.strip()] = ''
    return(modulesAndVersions, modules)

# get_modules_and_versions('./softwares/stampede-2_modules.txt')