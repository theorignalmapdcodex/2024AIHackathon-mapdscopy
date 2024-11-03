from app import main

query = "I lost my black cup, my precious cup, where is the last place I put it?"
print("Query:", query)
result = main(query)
print("Result:", result[0])
print("Video URL:", result[1]["video_uri"])
print("Start Time:", result[1]["start_time"])
print("End Time:", result[1]["end_time"])