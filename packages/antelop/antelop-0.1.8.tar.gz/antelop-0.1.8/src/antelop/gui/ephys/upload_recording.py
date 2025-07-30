import streamlit as st
import json
from antelop.utils.streamlit_utils import dropdown_insert_table
from antelop.utils.antelop_utils import get_cluster_path
from antelop.utils.datajoint_utils import upload, check_session
from antelop.utils.multithreading_utils import upload_thread_pool
from antelop.utils.external_utils import cluster_upload, check_upload_progress
import pandas as pd


def show(username, tables):
	col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

	with col2:
		st.title("Session")
		st.subheader("Upload a raw electrophysiology recording")

		st.divider()

		# get user to interactively insert table attributes
		tablename, insert_dict = dropdown_insert_table(
			tables, {"Recording": tables["Recording"]}, username, headless=True
		)

		# if upstream tables not populated, print error
		if tablename is None:
			st.text("")
			st.error(
				"""You can't upload a recording yet as you haven't got entries in the necessary upstream tables."""
			)
			st.warning(
				"Please make sure you have a session for which you can upload a recording."
			)
			st.stop()

		st.text("")

		cluster_path = get_cluster_path(insert_dict["recording"])
		upload_cluster_side = False

		if cluster_path is not None:

			upload_cluster_side = st.checkbox(
				"Upload on the cluster?",
				value=True,
				help="If checked, the recording will be uploaded on the cluster. which can be faster. If unchecked, the recording will be uploaded locally.",
			)
			st.text("")
			password = st.text_input(
				"Cluster password",
				type="password",
			)

		# add insert button
		if st.button("Insert"):
			# check user only inserting their own data
			if insert_dict["experimenter"] == username:
				# if directory has correct files and there's not already a recording, upload in separate thread
				status = (
					len(
						tables["Recording"]
						& {
							key: val
							for key, val in insert_dict.items()
							if key
							in [
								"experimenter",
								"experiment_id",
								"animal_id",
								"session_id",
							]
						}
					)
					== 0
				)
				if check_session(tables, insert_dict) and status:


					if upload_cluster_side:
						# if the user has selected to upload on the cluster, set the path to the cluster path
						insert_dict["recording"] = str(cluster_path)

						if 'device_channel_mapping' in insert_dict.keys():
							with open(insert_dict['device_channel_mapping']) as f:
								device_channel_mapping = json.load(f)
							insert_dict['device_channel_mapping'] = device_channel_mapping

						cluster_upload("Recording", insert_dict, password, str(insert_dict['recording']))
						st.success("Upload in progress!")
						st.info("You will get an email notification when the upload is complete.")

					else:

						# retrieve thread pool
						up_thread_pool = upload_thread_pool()

						# submit job to thread pool
						future = up_thread_pool.submit(
							upload,
							tablename,
							insert_dict,
							username=st.session_state.username,
							password=st.session_state.password,
						)

						# append future to session state
						st.session_state.upload_futures.append(
							(future, tablename, insert_dict)
						)

						st.text("")
						st.success("Upload in progress!")

				elif not status:
					st.text("")
					st.error("A recording already exists for this session.")

				# otherwise print error
				else:
					equip_type = insert_dict["ephys_acquisition"]
					st.text("")
					st.error("Recording directory does not contain correct files!")
					st.text("")
					st.warning(
						f"Please read the {equip_type} documentation to see what files are required."
					)
					if 'device_channel_mapping' in insert_dict.keys():
						st.warning("Alternatively your channel mapping file may be incorrect.")

			# otherwise print error
			else:
				st.text("")
				st.error("You can only insert your own data!")

		st.text("")

		# notice
		st.info(
			"Note that uploading large session recordings can take a while. This will occur in a separate thread so you can still use Antelop while the upload is occurring, and can use the button below to check your upload status."
		)

		st.text("")

		# add a button which shows upload statuses
		# uses all uploads in current session stored in session state
		# only shows if there are any downloads in this session

		if "upload_futures" in st.session_state:
			if st.button("Check insert progress"):
				# if there are any downloads this session
				if "upload_futures" in st.session_state:
					st.write("Upload statuses:")

					# initialise data
					display_futures = []

					# compute job statuses
					for (
						future,
						tablename,
						insert_dict,
					) in st.session_state.upload_futures:
						# compute statuses
						if future.done():
							if future.exception():
								status = "upload error"
							else:
								status = "upload success"
						else:
							status = "upload in progress"

						# primary keys for display
						keys = {
							key: val
							for key, val in insert_dict.items()
							if key in tables[tablename].primary_key
						}
						display = "-".join([str(i) for i in keys.values()])

						display_futures.append((tablename, display, status))

					# make dataframe to display
					df = pd.DataFrame(
						display_futures, columns=["Table", "Primary Key", "Status"]
					)

					# show dataframe
					st.dataframe(df, hide_index=True)

				# if there are no downloads in this session
				else:
					st.write("No uploads underway.")

		# if there are any uploads this session
		if "upload_cluster_jobs" in st.session_state:
			# button which shows spikesort statuses
			if st.button("Check upload progress"):
				check_upload_progress()