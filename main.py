import numpy as np
from statistics import mean
import functions
import pandas as pd

activity_labels = ["WALKING", "WALKING_UPSTAIRS", "WALKING_DOWNSTRAIRS", "SITTING", "STANDING", "LAYING",
                   "STAND_TO_SIT", "SIT_TO_STAND", "SIT_TO_LIE", "LIE_TO_SIT", "STAND_TO_LIE", "LIE_TO_STAND"]


def main():
	# retrieve data from txt files
	print("-------------------------------\nObtaining data from txt files...")
	path_to_labels = "HAPT_DATA_set\\RawData\\labels.txt"
	path_to_exp = "HAPT_data_set\\RawData\\acc_exp"
	info_users, info_labels = functions.retrieve_data(path_to_labels, path_to_exp)
	print("Data retrieved!\n-------------------------------\n")

	window = "gauss (size/5)"

	all_experiences = functions.fourier(info_labels, window, info_users)

	# functions.extract_data(info_labels)

	# single_experience ---> vários arrays de [N_EXP, N_USER, LABEL, XMIN, XMAX, DFTX, DFTY, DFTZ]
	# allexperiences ------> [single_experience1, single_experience2, ...]

	# EIXOS X Y Z para user tal
	# info_users -> acc_expXX_userYY.txt
	#                0.4333333437219827 0.01944444533917746 0.8930556332257938
	#                0.4277777761889662 0.01805555649491447 0.8763889306267443
	#                0.4402778031382534 -0.004166666912662869 0.9027777791608564
	#                0.4402778031382534 -0.004166666912662869 0.9027777791608564
	#                ...

	# experiência X, user Y, atividade Z, inicio do intervalo da atividade, fim do intervalo da atividade
	# info_labels -> labels.txt
	#                26 13 5 304 1423
	#                26 13 7 1574 1711
	#                26 13 4 1712 2616
	#                26 13 8 2617 2758
	#                ...

	while True:
		# main menu
		functions.main_menu()
		choice = int(input())

		if choice == 1:
			print("\nPlotting all experiences...")
			functions.ex2(info_labels, info_users)
			print("Plot successful!\n")

		elif choice == 2:
			functions.all_dft_menu()
			window = input("New window: ")
			all_experiences = functions.fourier(info_labels, window, info_users)

		elif choice == 3:
			while True:
				functions.single_dft_menu()
				user_input = input().split()
				n_exp, n_user, label, window = int(user_input[0]), int(user_input[1]), user_input[2], user_input[3]
				while functions.validate_data(n_exp, n_user, label) is False:
					user_input = input().split()
					n_exp, n_user, label, window = int(user_input[0]), int(user_input[1]), user_input[2], user_input[3]

				label_intervals = functions.fourier_single(info_labels, label, window, info_users[n_exp - 26], n_exp,
				                                           n_user)
				break

		elif choice == 4:
			functions.experience_menu()
			user_input = int(input())
			while functions.validate_experience(user_input) is False:
				user_input = int(input())
			functions.plot_activity(all_experiences[user_input - 26], window)
			# functions.plot_activity_nowindow(all_experiences[user_input - 26])

		elif choice == 5:
			# functions.feature_model_menu()
			user_input = input("Usage: <activity / activity_type> <test_size>\n").split()
			functions.sklearn_feature_extraction(user_input[0], float(user_input[1]))

		elif choice == 6:
			print("Steps per minute")
			user_input = input("Usage: <experience> for single experience or <ALL> for all steps between experiences.\n")

			if user_input == "ALL":
				print("Steps for all experiences:")
				functions.get_all_experience_steps(all_experiences, to_excel=False, debug=False)

			else:
				print("Steps for single experience:")
				functions.get_max_frequencies(all_experiences[int(user_input)-26], debug=False)

		elif choice == 7:
			print("Calculate sensibility/specificity")
			functions.calculate_sensibility_specificity(input("Usage: <activity_name>/<activity_type>/<all>\n"))

		elif choice == 8:
			n_exp = 26
			functions.calc_stft(info_users[n_exp - 26], n_exp)

		elif choice == 9:
			break

		else:
			print("Wrong option. Try again...")


if __name__ == "__main__":
	main()
