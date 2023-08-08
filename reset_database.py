from models import db
from models.rps import RPS
from models.jobClass import JobClass
from models.rpJobClass import RpJobClass
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField
from models.software import Software
from models.rpSoftware import RpSoftware
from models.gui import GUI
from models.rpGUI import RpGUI
from models.rpMemory import RpMemory
from models.rpInfo import RpInfo
from logic.rp_modules import get_modules_and_versions
import glob #for reading the text files
import os

db.connect()
tables = db.get_tables()
print(f"the tables: {tables}")

# delete all data and create blank tables
db.drop_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField,Software,RpSoftware,GUI,RpGUI,RpMemory,RpInfo])
db.create_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField,Software,RpSoftware,GUI,RpGUI,RpMemory,RpInfo])

rps = [
    {"name":"ACES", "scratch_tb":1, "longterm_tb":100, "graphical":2},
    {"name":"Anvil", "scratch_tb":100, "longterm_tb":50},
    {"name":"Bridges-2", "scratch_tb":0, "longterm_tb":0, "parallel": 1, "graphical":2},
    {"name":"DARWIN", "scratch_tb":2, "longterm_tb":10, "parallel": 1, "graphical":2},
    {"name":"Delta", "scratch_tb":1.5, "longterm_tb":0.5, "parallel": 1, "graphical":2},
    {"name":"Expanse", "scratch_tb":7000, "longterm_tb":12000, "parallel": 1, "graphical":2},
    {"name":"FASTER", "scratch_tb":1, "longterm_tb":50, "graphical":2},
    {"name":"Jetstream2", "scratch_tb":0, "longterm_tb":0, "virtual_machine":2, "always_running":2},
    {"name":"OOKAMI", "scratch_tb":30, "longterm_tb":80},
    {"name":"KyRIC", "scratch_tb":10, "longterm_tb":0.5, "graphical":2},
    {"name":"Rockfish", "scratch_tb":10, "longterm_tb":100},
    {"name":"Stampede-2", "scratch_tb":0, "longterm_tb":1, "parallel": 1, "graphical":2},
    {"name":"RANCH", "scratch_tb":0, "longterm_tb":20},
    {"name":"Open Science Grid", "scratch_tb":0, "longterm_tb":0.5},
    {"name":"Open Storage Network", "scratch_tb":0, "longterm_tb":0},
    ]
print("Adding RPS data")
RPS.insert_many(rps).on_conflict_replace().execute()

fields = [
    {"field_name":"Biology"},
    {"field_name":"Chemistry"},
    {"field_name":"Physics"},
    {"field_name":"Computer Science"},
    {"field_name":"Civil Engineering"},
    {"field_name":"Economics"},
    {"field_name":"Linguistics"},
    {"field_name":"History"},
    {"field_name":"Agriculture"},
    {"field_name":"Medicine"},
]
print("Adding ResearchFields data")
ResearchFields.insert_many(fields).on_conflict_replace().execute()

rpResearch = [
    {"rp": RPS.get(RPS.name == "Bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Biology"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "stampede-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Biology"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "expanse"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Biology"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Chemistry"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "stampede-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Chemistry"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Physics"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "stampede-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Physics"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "expanse"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Physics"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Computer Science"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "stampede-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Computer Science"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "expanse"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Computer Science"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "jetstream2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Civil Engineering"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Civil Engineering"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "jetstream2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Economics"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "expanse"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Economics"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "open science grid"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Linguistics"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "open science grid"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "History"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "kyric"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Agriculture"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "anvil"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Agriculture"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "ookami"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Medicine"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "rockfish"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Medicine"),
     "suitability":1,
    },
    {"rp": RPS.get(RPS.name == "bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Medicine"),
     "suitability":1,
    },
]
print("Adding RpResearchField data")
RpResearchField.insert_many(rpResearch).on_conflict_replace().execute()

jobClass = [
    {"class_name":"Data Analytics"},
    {"class_name":"Data Mining"},
    {"class_name":"NLP"},
    {"class_name":"Textual Analysis"},
    {"class_name":"Modeling and Simulation"},
    {"class_name":"Bioinformatics"},
    {"class_name":"Biophysics"},
    {"class_name":"BioChemistry"},
    {"class_name":"Fluid Dynamics"},
    {"class_name":"Image Processing"},
    {"class_name":"Machine Learning"},
    {"class_name": "Materials Science"},
    {"class_name":"Astronomic Science"},
    {"class_name":"Digital Humanities"},
    {"class_name":"Computational Chemistry"},
    {"class_name":"Genomics"},
    {"class_name":"Deep Learning"},
    {"class_name":"High Energy Physics"},
    {"class_name":"Virtual Machine"},
    {"class_name":"General"},
    {"class_name":"Parallel"},
]
print("Adding JobClass data")
JobClass.insert_many(jobClass).on_conflict_replace().execute()

#Class of jobs
jobClassAndRps = {"Data Analytics":['delta', 'bridges-2', 'darwin'],
                 "Data Mining":['darwin'],
                 "NLP":['kyric'],
                 "Textual Analysis":['delta'],
                 "Modeling and Simulation":['delta'],
                 "Bioinformatics":['kyric','expanse'],
                 "Biophysics":['kyric','expanse'],
                 "Biochemistry":['kyric','expanse'],
                 "Fluid Dynamics":['delta'],
                 "Materials Science":['expanse'], 
                 "Image Processing":['darwin'], 
                 "Machine Learning":['delta','bridges-2','darwin'],
                 "Astronomic Science":['expanse'], 
                 "Digital Humanities":[], 
                 "Computational Chemistry":['expanse'], 
                 "Genomics":[], 
                 "Deep Learning":['delta'], 
                 "High Energy Physics":['expanse'],
                 "Virtual Machine":['jetstream2'], 
                 "General":['stampede-2','darwin'], 
                 "Parallel":['stampede-2']}

rpJobClass = []
for jobClass in list(jobClassAndRps.keys()):
    for rp in jobClassAndRps[jobClass]:
        rpJobClass.append({"rp": RPS.get(RPS.name == rp),
        "job_class": JobClass.get(JobClass.class_name == jobClass),
        "suitability":1,
        })
print("Adding RPJobClass data")
RpJobClass.insert_many(rpJobClass).on_conflict_replace().execute()

Gui = [
    {"gui":"OpenOnDemand"},
    {"gui":"RStudio"},
    {"gui":"JupyterLab"},
    {"gui":"Exosphere"},
    {"gui":"Horizon"},
    {"gui":"CACAO"},
    ]

print("Adding GUI data")
GUI.insert_many(Gui).on_conflict_replace().execute()

#Types of GUI's

rpGUI_together = {
    "OpenOnDemand":['bridges-2', 'expanse', 'anvil', 'aces', 'faster'],
    "RStudio":['aces'],
    "JupyterLab":['aces'],
    "Exosphere":['jetstream2'],
    "Horizon":['jetstream2'],
    "CACAO":['jetstream2']}

rpGui = []
for gui in list(rpGUI_together.keys()):
    for rp in rpGUI_together[gui]:
        rpGui.append({"rp": RPS.get(RPS.name == rp),
        "rp_gui": GUI.get(GUI.gui == gui)})

print("Adding the GUI to the RP list")
RpGUI.insert_many(rpGui).on_conflict_replace().execute()

#Accessing all of the module text files and putting them into their respective arrays

os.chdir('softwares')

modules = glob.glob('*.txt')
rpSftw = {}
modulesAndVersions = {}
for name in modules:
    rpName = name.split("_")[0]
    modulesAndVersions,mods = get_modules_and_versions(name,modulesAndVersions)
    rpSftw[rpName] = mods

print("Adding data to Software")
Software.insert_many(modulesAndVersions.items(), fields=[Software.software_name,Software.version]).on_conflict_replace().execute()

#associate modules with specific RP
rpSoftware = []
for item in rpSftw.items():
    rp = RPS.get(RPS.name == item[0])
    rpSoftware.extend([(rp,Software.get(Software.software_name==software),1) for software in item[1]])


print("Adding data to RpSoftware")
RpSoftware.insert_many(rpSoftware,fields=[RpSoftware.rp,RpSoftware.software,RpSoftware.suitability]).on_conflict_replace().execute()

#per node memory
per_node_memory_gb = [{'rp':RPS.get(RPS.name == 'aces'),
                    'node_type':'Standard','per_node_memory':512},
                   {'rp':RPS.get(RPS.name == 'anvil'),
                    'node_type':'Standard','per_node_memory':256},
                   {'rp':RPS.get(RPS.name == 'anvil'), 
                    'node_type':'Large Memory', 'per_node_memory':1000},
                   {'rp':RPS.get(RPS.name == 'bridges-2'),
                    'node_type':'Standard','per_node_memory':256},
                   {'rp':RPS.get(RPS.name == 'bridges-2'),
                    'node_type':'Large Memory','per_node_memory':512},
                   {'rp':RPS.get(RPS.name == 'darwin'),
                    'node_type':'Standard','per_node_memory':512},
                   {'rp':RPS.get(RPS.name == 'darwin'),
                    'node_type':'Large Memory','per_node_memory':1024},
                   {'rp':RPS.get(RPS.name == 'darwin'),
                    'node_type':'Extra-Large Memory','per_node_memory':2048},
                   {'rp':RPS.get(RPS.name == 'delta'),
                    'node_type':'Standard','per_node_memory':256},
                   {'rp':RPS.get(RPS.name == 'delta'),
                    'node_type':'Large Memory','per_node_memory':2000},
                   {'rp':RPS.get(RPS.name == 'expanse'),
                    'node_type':'Standard','per_node_memory':256},
                   {'rp':RPS.get(RPS.name == 'expanse'),
                    'node_type':'Large Memory','per_node_memory':2000},
                   {'rp':RPS.get(RPS.name == 'faster'),
                    'node_type':'Standard','per_node_memory':256},
                   {'rp':RPS.get(RPS.name == 'jetstream2'),
                    'node_type':'Standard','per_node_memory':512},
                   {'rp':RPS.get(RPS.name == 'jetstream2'),
                    'node_type':'Large Memory','per_node_memory':1024},
                   {'rp':RPS.get(RPS.name == 'ookami'),
                    'node_type':'Standard','per_node_memory':32},
                   {'rp':RPS.get(RPS.name == 'kyric'),
                    'node_type':'Large Memory','per_node_memory':3000},
                   {'rp':RPS.get(RPS.name == 'rockfish'),
                    'node_type':'Standard','per_node_memory':192},
                   {'rp':RPS.get(RPS.name == 'rockfish'),
                    'node_type':'Large Memory','per_node_memory':1500},
                   {'rp':RPS.get(RPS.name == 'stampede-2'),
                    'node_type':'Standard','per_node_memory':96}]
print('Adding data to RpMemory')
RpMemory.insert_many(per_node_memory_gb,fields=[RpMemory.rp,RpMemory.node_type,RpMemory.per_node_memory_gb]).on_conflict_replace().execute()

#info about the RP's as well as links to their websites
rpInfo = [{'rp':RPS.get(RPS.name == 'aces'), 'blurb': r"ACES (Accelerating Computing for Emerging Sciences) is funded by NSF ACSS program (Award #2112356) and provides an innovative advanced computational prototype system. The ACES system has Intel Sapphire Rapids processors, Graphcore IPUs, NEC Vector Engines, Intel Max GPUs (formerly Ponte Vecchio), Intel FPGAs, Next Silicon co-processors, NVIDIA H100 GPUs, Intel Optane memory, and LIQID's composable PCIe fabric.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'anvil'), 'blurb': r"Purdue's Anvil cluster is comprised of 1000 nodes (each with 128 cores and 256 GB of memory for a peak performance of 5.3 PF), 32 large memory nodes (each with 128 cores and 1 TB of memory), and 16 GPU nodes (each with 128 cores, 256 GB of memory, and four NVIDIA A100 Tensor Core GPUs) providing 1.5 PF of single-precision performance to support machine learning and artificial intelligence applications. All CPU cores are AMD's 'Milan' architecture running at 2.0 GHz, and all nodes are interconnected using a 100 Gbps HDR Infiniband fabric. Scratch storage consists of a 10+ PB parallel filesystem with over 3 PB of flash drives. Storage for active projects is provided by Purdue's Research Data Depot, and data archival is available via Purdue's Fortress tape archive. The operating system is CentOS 8, and the batch scheduling system is Slurm. Anvil's advanced computing capabilities are well suited to support a wide range of computational and data-intensive research spanning from traditional high-performance computing to modern artificial intelligence applications.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'bridges-2'), 'blurb': r"Bridges-2 Regular Memory (RM) nodes provide extremely powerful general-purpose computing, machine learning and data analytics, AI inferencing, and pre- and post-processing. Each Bridges RM node consists of two AMD EPYC “Rome” 7742 64-core CPUs, 256-512GB of RAM, and 3.84TB NVMe SSD. 488 Bridges-2 RM nodes have 256GB RAM, and 16 have 512GB RAM for more memory-intensive applications (see also Bridges-2 Extreme Memory nodes, each of which has 4TB of RAM). Bridges-2 RM nodes are connected to other Bridges-2 compute nodes and its Ocean parallel filesystem and archive by HDR-200 InfiniBand.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'darwin'), 'blurb': r"The Delaware Advanced Research Workforce and Innovation Network (DARWIN) computing system at the University of Delaware is based on AMD Epyc™ 7502 processors with three main memory sizes to support different workload requirements (512 GiB, 1024 GiB, 2048 GiB). The cluster provides more than 1 PiB usable, shared storage via a dedicated Lustre parallel file system to support large, data sciences workloads. The Mellanox HDR 200Gbps InfiniBand network provides near-full bisectional bandwidth at 100 Gbps per node.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'delta'), 'blurb': r"The NCSA Delta CPU allocation type provides access to the Delta CPU-only nodes. The Delta CPU resource comprises 124 dual-socket compute nodes for general purpose computation across a broad range of domains able to benefit from the scalar and multi-core performance provided by the CPUs, such as appropriately scaled weather and climate, hydrodynamics, astrophysics, and engineering modeling and simulation, and other domains using algorithms not yet adapted for the GPU. Each Delta CPU node is configured with 2 AMD EPYC 7763 ('Milan') processors with 64-cores/socket (128-cores/node) at 2.55GHz and 256GB of DDR4-3200 RAM. An 800GB, NVMe solid-state disk is available for use as local scratch space during job execution. All Delta CPU compute nodes are interconnected to each other and to the Delta storage resource by a 100 Gb/sec HPE Slingshot network fabric.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'expanse'), 'blurb': r"Expanse will be a Dell integrated compute cluster, with AMD Rome processors, interconnected with Mellanox HDR InfiniBand in a hybrid fat-tree topology. There are 728 compute nodes, each with two 64-core AMD EPYC 7742 (Rome) processors for a total of 93,184 cores. They will feature 1TB of NVMe storage and 256GB of DRAM per node. Full bisection bandwidth will be available at rack level (56 nodes) with HDR100 connectivity to each node. HDR200 switches are used at the rack level and there will be 3:1 oversubscription cross-rack. In addition, Expanse also has four 2 TB large memory nodes. The system will also feature 12PB of Lustre based performance storage (140GB/s aggregate), and 7PB of Ceph based object storage.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'faster'), 'blurb': r"FASTER (Fostering Accelerated Scientific Transformations, Education and Research) is funded by the NSF MRI program (Award #2019129) and provides a composable high-performance data-analysis and computing instrument. The FASTER system has 180 compute nodes with 2 Intel 32-core Ice Lake processors and includes 260 NVIDIA GPUs (40 A100, 8 A10, 4 A30, 8 A40 and 200 T4 GPUs). Using LIQID's composable technology, all 180 compute nodes have access to the pool of available GPUs, dramatically improving workflow scalability. FASTER has HDR InfiniBand interconnection and access to a 5PB of shared usable high-performance storage system running Lustre filesystem. Thirty percent of FASTER's computing resources will be allocated to researchers nationwide through the ACCESS AARC process.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'jetstream2'), 'blurb': r"Jetstream2 is a user-friendly cloud environment designed to give researchers and students access to computing and data analysis resources on demand as well as for gateway and other infrastructure projects. Jetstream2 is a hybrid-cloud platform that provides flexible, on-demand, programmable cyberinfrastructure tools ranging from interactive virtual machine services to a variety of infrastructure and orchestration services for research and education. The primary resource is a standard CPU resource consisting of AMD Milan 7713 CPUs with 128 cores per node and 512gb RAM per node connected by 100gbps ethernet to the spine.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'ookami'), 'blurb': r"Ookami is a computer technology testbed supported by the National Science Foundation under grant OAC 1927880. It provides researchers with access to the A64FX processor developed by Riken and Fujitsu for the Japanese path to exascale computing and is deployed in the, until June 2022, fastest computer in the world, Fugaku. It is the first such computer outside of Japan. By focusing on crucial architectural details, the ARM-based, multi-core, 512-bit SIMD-vector processor with ultrahigh-bandwidth memory promises to retain familiar and successful programming models while achieving very high performance for a wide range of applications. While being very power-efficient it supports a wide range of data types and enables both HPC and big data applications. The Ookami HPE (formerly Cray) Apollo 80 system has 176 A64FX compute nodes each with 32GB of high-bandwidth memory and a 512 Gbyte SSD. This amounts to about 1.5M node hours per year. A high-performance Lustre filesystem provides about 0.8 Pbyte storage. To facilitate users exploring current computer technologies and contrasting performance and programmability with the A64FX, Ookami also includes: - 1 node with dual socket AMD Milan (64cores) with 512 Gbyte memory - 2 nodes with dual socket Thunder X2 (64 cores) each with 256 Gbyte memory - 1 node with dual socket Intel Skylake (32 cores) with 192 Gbyte memory and 2 NVIDIA V100 GPUs", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'kyric'), 'blurb': r"Five large memory compute nodes dedicated for XSEDE allocation. Each of these nodes have 40 cores (Broadwell class and lntel(R) Xeon(R) CPU E7-4820 v4 @ 2.00GHz with 4 sockets, 10 cores/socket), 3TB RAM, and 6TB SSD storage drives. The 5 dedicated XSEDE nodes will have exclusive access to approximately 300 TB of network attached disk storage. All these compute nodes are interconnected through a 100 Gigabit Ethernet (l00GbE) backbone and the cluster login and data transfer nodes will be connected through a 100Gb uplink to lnternet2 for external connections.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'rockfish'), 'blurb': r"Johns Hopkins University will participate in the ACCESS Federation with its new NSF-funded flagship cluster 'rockfish.jhu.edu' funded by NSF MRI award #1920103 that integrates high-performance and data-intensive computing while developing tools for generating, analyzing and disseminating data sets of ever-increasing size. The cluster will contain compute nodes optimized for different research projects and complex, optimized workflows. Rockfish (368) Regular Memory nodes are intended for regular-purpose computing, machine learning and data analytics. Each regular compute node consists of two Intel Xeon Gold Cascade Lake (6248R) processors with 192GB of memory, 3.0GHz base frequency, 48 cores per node and 1TB NVMe for local storage. All compute nodes have HDR100 connectivity. In addition, the cluster has access to several GPFS file systems totaling 10PB of storage. 20% of these resources will be allocated via ACCESS.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'stampede-2'), 'blurb': r"The Stampede2 Dell/Intel Knights Landing (KNL), Skylake (SKX) System provides the user community access to two Intel Xeon compute technologies. The system is configured with 4204 Dell KNL compute nodes, each with a stand-alone Intel Xeon Phi Knights Landing bootable processor. Each KNL node includes 68 cores, 16GB MCDRAM, 96GB DDR-4 memory and a 200GB SSD drive. Stampede2 also includes 1736 Intel Xeon Skylake (SKX) nodes and additional management nodes. Each SKX includes 48 cores, 192GB DDR-4 memory, and a 200GB SSD. Allocations awarded on Stampede2 may be used on either or both of the node types. Compute nodes have access to dedicated Lustre Parallel file systems totaling 28PB raw, provided by Cray. An Intel Omni-Path Architecture switch fabric connects the nodes and storage through a fat-tree topology with a point to point bandwidth of 100 Gb/s (unidirectional speed). 16 additional login and management servers complete the system. Stampede2 will deliver an estimated 18PF of peak performance. Please see the Stampede2 User Guide for detailed information on the system and how to most effectively use it. https://portal.xsede.org/tacc-stampede2", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'ranch'), 'blurb': r"TACC's High Performance Computing systems are used primarily for scientific computing with users having access to WORK, SCRATCH, and HOME file systems that are limited in size. This is also true for TACC's visualization system, Longhorn. The Ranch system serves the HPC and Vis community systems by providing a massive, high-performance file system for archival purposes. Space on Ranch can also be requested independent of an accompanying allocation on an XSEDE compute or visualization resource. Please note that Ranch is an archival system. The ranch system is not backed up or replicated. This means that Ranch contains a single copy, and only a single copy, of your file/s. While lost data due to tape damage is rare, please keep this fact in mind for your data management plans.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'open science grid'), 'blurb': r"A virtual HTCondor pool made up of resources from the Open Science Grid. High throughput jobs using a single core, or a small number of threads which can fit on a single compute node.", 'link': r"https://allocations.access-ci.org/resources"},
          {'rp':RPS.get(RPS.name == 'open storage network'), 'blurb': r"The Open Storage Network (OSN) is an NSF-funded cloud storage resource, geographically distributed among several pods. OSN pods are currently hosted at SDSC, NCSA, MGHPCC, RENCI, and Johns Hopkins University. Each OSN pod currently hosts 1PB of storage, and is connected to R&E networks at 50 Gbps. OSN storage is allocated in buckets, and is accessed using S3 interfaces with tools like rclone, cyberduck, or the AWS cli.", 'link': r"https://allocations.access-ci.org/resources"}]
print('Adding data to RpInfo')
RpInfo.insert_many(rpInfo,fields=[RpInfo.rp,RpInfo.blurb,RpInfo.link]).on_conflict_replace().execute()
#close the database
db.close()