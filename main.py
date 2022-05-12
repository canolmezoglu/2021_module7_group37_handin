# imports #############################################################################
from time import time
from graph_io import load_graph
from refinement import uniform_partitions, hopcroft_refinement, refine_partitions_by_color_group_size
from equivalence import equivalence_classes_main
from auto import automorphism_main

# variables for use in main function ##################################################
graph_dictionary = dict()

# add list of names of the graphs from SampleGraphsSetBasicColorRefinement.zip to the graph_dictionary
basic_colorref_set = ["graphs/cref9vert_4_9.grl",
                      "graphs/colorref_smallexample_6_15.grl",
                      "graphs/colorref_smallexample_4_16.grl",
                      "graphs/colorref_smallexample_4_7.grl",
                      "graphs/colorref_smallexample_2_49.grl",
                      "graphs/colorref_largeexample_6_960.grl",
                      "graphs/colorref_largeexample_4_1026.grl"]
graph_dictionary["basic_colorref_set"] = basic_colorref_set

# add list of names of graphs of the "big trees" type to the graph_dictionary
bigtrees_set = ["graphs/bigtrees1.grl",
                "graphs/bigtrees2.grl",
                "graphs/bigtrees3.grl"]
graph_dictionary["bigtrees_set"] = bigtrees_set

# add list of names of graphs of the "cographs" type to the graph_dictionary
cographs_set = ["graphs/cographs1.grl"]
graph_dictionary["cographs_set"] = cographs_set

# add list of names of graphs of the "cubes" type to the graph_dictionary
cubes_set = ["graphs/cubes3.grl",
             "graphs/cubes4.grl",
             "graphs/cubes5.grl",
             "graphs/cubes6.grl",
             "graphs/cubes7.grl",
             "graphs/cubes8.grl",
             "graphs/cubes9.grl"]
graph_dictionary["cubes_set"] = cubes_set
# add list of names of graphs of the "modules" type to the graph_dictionary
modules_set = ["graphs/modulesC.grl",
               "graphs/modulesD.grl"]
graph_dictionary["modules_set"] = modules_set

# add list of names of graphs of the "products" type to the graph_dictionary
products_set = ["graphs/products72.grl",
                "graphs/products216.grl"]
graph_dictionary["products_set"] = products_set

# add list of names of graphs of the "torus" type to the graph_dictionary
torus_set = ["graphs/torus24.grl",
             "graphs/torus72.grl",
             "graphs/torus144.grl"]
graph_dictionary["torus_set"] = torus_set

# add list of names of graphs of the "torus" type to the graph_dictionary
trees_set = ["graphs/trees11.grl",
             "graphs/trees36.grl",
             "graphs/trees90.grl"]
graph_dictionary["trees_set"] = trees_set

# add list of names of graphs of the "wheeljoin" type to the graph_dictionary
wheeljoin_set = ["graphs/wheeljoin14.grl",
                 "graphs/wheeljoin19.grl",
                 "graphs/wheeljoin25.grl",
                 "graphs/wheeljoin33.grl"]
graph_dictionary["wheeljoin_set"] = wheeljoin_set

# add list of names of graphs of the "wheelstar" type to the graph_dictionary
wheelstar_set = ["graphs/wheelstar12.grl",
                 "graphs/wheelstar15.grl",
                 "graphs/wheelstar16.grl"]
graph_dictionary["wheelstar_set"] = wheelstar_set

# add list of names of the graphs from SampleGraphsSetBranching.zip to the graph_dictionary
branching_set = (bigtrees_set +
                 cographs_set +
                 cubes_set +
                 modules_set +
                 products_set +
                 torus_set +
                 trees_set +
                 wheeljoin_set +
                 wheelstar_set)
graph_dictionary["branching_set"] = branching_set

# add list of names of the graphs from SampleGraphsSetFastColorRefinement.zip to the graph_dictionary
fast_colorref_set = ["graphs/threepaths5.gr",
                     "graphs/threepaths10.gr",
                     "graphs/threepaths20.gr",
                     "graphs/threepaths40.gr",
                     "graphs/threepaths80.gr",
                     "graphs/threepaths160.gr",
                     "graphs/threepaths320.gr",
                     "graphs/threepaths640.gr",
                     "graphs/threepaths1280.gr",
                     "graphs/threepaths2560.gr",
                     "graphs/threepaths5120.gr",
                     "graphs/threepaths10240.gr"]
graph_dictionary["fast_colorref_set"] = fast_colorref_set

basic_set = ["graphs/basic/basicAut1.gr",
             "graphs/basic/basicAut2.gr",
             "graphs/basic/basicGI1.grl",
             "graphs/basic/basicGI2.grl",
             "graphs/basic/basicGI3.grl",
             "graphs/basic/basicGIAut1.grl"]
graph_dictionary["basic_set"] = basic_set

bonus_aut_set = ["graphs/bonus/bonusAut1.gr",
                 "graphs/bonus/bonusAut2.gr",
                 "graphs/bonus/bonusAut3.grl",
                 "graphs/bonus/bonusAut4.grl",
                 "graphs/bonus/bonusAut5.grl"]
graph_dictionary["bonus_aut_set"] = bonus_aut_set

bonus_GI_set = ["graphs/bonus/bonusGI1.grl",
                "graphs/bonus/bonusGI2.grl",
                "graphs/bonus/bonusGI3.grl",
                "graphs/bonus/bonusGI4.grl",
                "graphs/bonus/bonusGI5.grl"]
graph_dictionary["bonus_GI_set"] = bonus_GI_set

# add list of names of all graphs used in the project session we currently have to the graph_dictionary
project_session_set = basic_set + bonus_aut_set + bonus_GI_set
graph_dictionary["project_session_set"] = project_session_set

# add list of names of all bonus graphs we currently have to the graph_dictionary
complete_bonus_set = bonus_aut_set + bonus_GI_set
graph_dictionary["complete_bonus_set"] = complete_bonus_set

# add list of names of all graphs we currently have to the graph_dictionary
complete_set = basic_colorref_set + fast_colorref_set + branching_set + project_session_set
graph_dictionary["complete_set"] = complete_set

# a list of names of all sets we have separated for ease of asking questions in main()
available_sets = ["basic_colorref_set",
                  "fast_colorref_set",
                  "branching_set",
                  "bigtrees_set",
                  "cographs_set",
                  "cubes_set",
                  "modules_set",
                  "products_set",
                  "torus_set",
                  "trees_set",
                  "wheeljoin_set",
                  "wheelstar_set",
                  "basic_set",
                  "bonus_aut_set",
                  "bonus_GI_set",
                  "project_session_set",
                  "complete_bonus_set",
                  "complete_set"]


def run(working_set, also_count_aut, timed):
    quickrun = ask_for_quickrun()

    if not quickrun:

        print(">>> WELCOME TO MANUAL CONFIGURATION")

        set_name = available_sets[ask_for_set()]

        working_set = graph_dictionary[set_name]

        file_number = ask_for_single_file(working_set)
        if file_number >= 0:
            working_set = [working_set[file_number]]

        also_count_aut = ask_for_isom_autom()

        timed = ask_for_time()

    print(">>> FINISHED CONFIGURATION\n\n")

    for file_location in working_set:
        with open(file_location) as file:
            print(">>> currently working on file:", file_location)

            # Load in the graphs at the current file location
            current_graph = load_graph(file, read_list=True)

            # Start time after reading the file, since we have very little influence on the efficiency of that
            start_time = time()

            # Color the graphs
            partitions, stack = uniform_partitions(current_graph[0])
            hopcroft_refinement(partitions, stack)
            refine_partitions_by_color_group_size(partitions)

            print("\nColored Graph, waiting for results:\n")

            # Assign partitions to the index of the graphs they originated from
            for graph_number in range(len(current_graph[0])):
                partitions[graph_number].graph_index = graph_number

            # get equivalence classes
            equivalence_classes = equivalence_classes_main(partitions)

            # if the also_count_aut boolean is set execute this to count automorphisms
            if also_count_aut:
                automorphism_main(equivalence_classes)

            result = ""

            for equivalence_class in equivalence_classes:

                partition_in_class = []
                for partition in equivalence_class.partitions:
                    partition_in_class.append(partition.graph_index)
                result += str(partition_in_class) + ";\n"

                if also_count_aut:
                    result += " #aut: " + str(equivalence_class.automorphisms)

                result += '\n'

            end_time = time()

            if timed:
                result += "time elapsed: " + str(end_time-start_time)

            print(result, '\n')


def ask_for_quickrun():
    print(">>> Leave the response blank to enter 'quickrun', responding anything else leads to config.")
    choice = input()
    return len(choice) == 0

def ask_for_set():
    print(">>> Please select the set of graph files you want to use: ")

    counter = 0
    for set_name in available_sets:
        counter += 1
        print("    ", counter, ": ", set_name)

    has_valid_input = False

    while not has_valid_input:
        choice = input()
        if choice.isnumeric():
            if 1 <= int(choice) <= len(available_sets):
                return int(choice) - 1

        print(">>> INVALID INPUT: please input the number associated with your choice")


def ask_for_single_file(graph_set):
    print(">>> do you want to evaluate the entire set you selected or only one file"
          "\n     0:  entire set")
    counter = 0
    for file in graph_set:
        counter += 1
        print("    ", counter, ": ", file)

    is_valid_choice = False

    while not is_valid_choice:
        choice = input()

        if choice.isnumeric():
            if 0 <= int(choice) <= len(graph_set):
                return int(choice) - 1

        print(">>> INVALID INPUT: please input the number associated with your choice")


def ask_for_isom_autom():
    print(">>> do you want to evaluate Automorphisms as well as Isomorphisms?",
          "\n     1 : yes"
          "\n     2 : no")

    has_valid_input = False

    while not has_valid_input:
        choice = input()
        if choice.isnumeric():
            if int(choice) == 1:
                print(">>> Automorphisms as well as Isomophisms will be evaluated\n")
                return True
            elif int(choice) == 2:
                print(">>> only Isomophisms will be evaluated\n")
                return False

        print(">>> INVALID INPUT: please input the number associated with your choice")


def ask_for_time():
    print(">>> do you want to time the processes",
          "\n     1 : yes"
          "\n     2 : no")

    has_valid_input = False

    while not has_valid_input:

        choice = input()

        if choice.isnumeric():
            if int(choice) == 1:
                print(">>> The processes will be timed\n")
                return True
            elif int(choice) == 2:
                print(">>> The processes will not be timed\n")
                return False

        print(">>> INVALID INPUT: please input the number associated with your choice")


# QUICKRUN configuration:
qr_graph_set = ["extra/competeAUT1.gr",
                "extra/competeGIAUT2.grl",
                "extra/competeGIAUT3.grl",
                "extra/competeGIAUT4.grl",
                "extra/competeGIAUT5.grl",
                "extra/competeGIAUT6.grl"]
qr_count_aut = True
qr_timed_run = True

#do not touch!
run(qr_graph_set, qr_count_aut, qr_timed_run)
