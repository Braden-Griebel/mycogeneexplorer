"""
Script to create metabolic graphs from the genome scale metabolic models
"""
# Core Library Imports
import os

# local imports
import mycogeneexplorer.gene_network as gn


base_fba_mode_path = os.path.join("..", "mycogeneexplorer", "data", "fba_models")
base_out_path = os.path.join("..", "mycogeneexplorer", "data", "metabolic_networks")

print("Reading in iEK1008 Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path, "iEK1008", "iEK1008.xml"), "xml")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "iEK1008_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "iEK1008_directed_network.json"))
print("Finished with iEK1008, Starting with iEK1011")

print("Reading in iEK1011_deJesusEssen_media Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "iEK1011",
                                                   "iEK1011 Models",
                                                   "iEK1011_deJesusEssen_media.json"), "json")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "iEK1011_deJesusEssen_media_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "iEK1011_deJesusEssen_media_directed_network.json"))
print("Finished with iEK1011_deJesusEssen_media, Starting with iEK1011_drugTesting_media")

print("Reading in iEK1011_drugTesting_media Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "iEK1011",
                                                   "iEK1011 Models",
                                                   "iEK1011_drugTesting_media.json"), "json")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path,"iEK1011_drugTesting_media_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "iEK1011_drugTesting_media_directed_network.json"))
print("Finished with iEK1011_drugTesting_media, Starting with iEK1011_griffinEssen_media")


print("Reading in iEK1011_griffinEssen_media Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "iEK1011",
                                                   "iEK1011 Models",
                                                   "iEK1011_griffinEssen_media.json"), "json")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "iEK1011_griffinEssen_media_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "iEK1011_griffinEssen_media_directed_network.json"))
print("Finished with iEK1011_griffinEssen_media, Starting with iEK1011_inVivo_media")

print("Reading in iEK1011_inVivo_media Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "iEK1011",
                                                   "iEK1011 Models",
                                                   "iEK1011_inVivo_media.json"), "json")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "iEK1011_inVivo_media_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "iEK1011_inVivo_media_directed_network.json"))
print("Finished with iEK1011_inVivo_media, Starting with iEK1011_m7H10_media")

print("Reading in iEK1011_m7H10_media Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "iEK1011",
                                                   "iEK1011 Models",
                                                   "iEK1011_m7H10_media.json"), "json")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "iEK1011_m7H10_media_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "iEK1011_m7H10_media_directed_network.json"))
print("Finished with iEK1011_m7H10_media, Starting with iEK1011_v2")

print("Reading in iEK1011_m7H10_media Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "iEK1011",
                                                   "iEK1011 Models",
                                                   "iEK1011_m7H10_media.json"), "json")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "iEK1011_m7H10_media_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "iEK1011_m7H10_media_directed_network.json"))
print("Finished with iEK1011_m7H10_media, Starting with iEK1011_v2")

print("Reading in iEK1011_v2 Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "iEK1011_v2",
                                                   "iEK1011_2.0.json"), "json")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "iEK1011_v2_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "iEK1011_v2_directed_network.json"))
print("Finished with iEK1011_v2, Starting with iNJ661")

print("Reading in iNJ661 Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "iNJ661",
                                                   "Jamshidi2007mtbBiGG.xml"), "sbml")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "iNJ661_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "iNJ661_directed_network.json"))
print("Finished with iNJ661, Starting with iSM810")

print("Reading in iSM810 Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "iSM810",
                                                   "iSM810anot.mat"), "mat")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "iSM810_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "iSM810_directed_network.json"))
print("Finished with iSM810, Starting with sMtb2")

print("Reading in sMtb2 Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "sMtb2",
                                                   "sMtb2.0.json"), "json")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "sMtb2_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "sMtb2_directed_network.json"))
print("Finished with sMtb2, Starting with Zimmerman")

print("Reading in Zimmerman Model")
model = gn.load_cobra_model_from_file(os.path.join(base_fba_mode_path,
                                                   "Zimmerman2017",
                                                   "modelIMPH_MTB_Cholesterol.mat"), "mat")
print("Creating Graph from Model")
graph = gn.create_metabolic_network(model)
print("Writing graph to file")
gn.write_network(graph, os.path.join(base_out_path, "zimmerman_network.json"))
print("Creating directed graph")
digraph = gn.create_directed_metabolic_network(model)
print("Writing Directed Graph to file")
gn.write_network(digraph, os.path.join(base_out_path, "zimmerman_directed_network.json"))
print("Finished with Zimmerman")

print("Finished with all models")