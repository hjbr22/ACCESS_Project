
def get_modules_and_versions(filename):
    """
    Takes as input a filename or path
    returns a nested list of modules where the first item 
    is the module name and the second is the module version

    The input file must contain the raw output gotten from running
    'module avail &> <file-name>.txt' on an RP
    """
    with open(filename) as stampede_mods:
        content = stampede_mods.read()
        content = content.split("Where:")[0]
        # content = content.split("\n")
        moduleAndVersion = []
        for i in content.split():
            if ("----" in i) or ("/opt" in i) or ("(L" in i) or ("D)" in i):
                pass
            else:
                # print("printing one \n", i, "\n")
                moduleAndVersion.append(i.split("/"))
    # print(moduleAndVersion)
    return(moduleAndVersion)