import os
import csv
import argparse

# Function to generate CSV files
def generate_csv_files(func_num, serve_time, output_dir="data/traces/example2"):
    # Create output directory if it doesn't exist
    output_dir = os.path.join("data/traces/example2", f"{func_num}_{serve_time}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file1name = f"dirigent.csv"
    file1path = os.path.join(output_dir, file1name)

    header1 = ["HashFunction", "Image", "Port", "Protocol", "ScalingUpperBound", "ScalingLowerBound", "IterationMultiplier"]
    row_data = ["c13acdc7567b225971cef2416a3a2b03c8a4d8d154df48afe75834e2f5c59ddf", "empty", "80", "tcp", "1", "0", "80"]

    with open(file1path, mode='w', newline='') as file1:
        writer = csv.writer(file1)
        writer.writerow(header1)
        for _ in range(func_num):
            writer.writerow(row_data)

    print(f"Generated {file1path}")

    file2name = f"durations.csv"
    file2path = os.path.join(output_dir, file2name)

    header2 = ["HashOwner","HashApp","HashFunction","Average","Count","Minimum","Maximum","percentile_Average_0","percentile_Average_1","percentile_Average_25","percentile_Average_50","percentile_Average_75","percentile_Average_99","percentile_Average_100"]
    row_data = ["c455703077a17a9b8d0fc655d939fcc6d24d819fa9a1066b74f710c35a43cbc8","68baea05aa0c3619b6feb78c80a07e27e4e68f921d714b8125f916c3b3370bf2","c13acdc7567b225971cef2416a3a2b03c8a4d8d154df48afe75834e2f5c59ddf","1",serve_time,serve_time,serve_time,serve_time,serve_time,serve_time,serve_time,serve_time,serve_time,serve_time]
    with open(file2path, mode='w', newline='') as file2:
        writer = csv.writer(file2)
        writer.writerow(header2)
        for _ in range(func_num):
            writer.writerow(row_data)

    print(f"Generated {file2path}")

    file3name = f"invocations.csv"
    file3path = os.path.join(output_dir, file3name)
    header3 = ["HashOwner","HashApp","HashFunction","Trigger","1","2","3","4","5","6","7","8","9","10"]
    row_data = ["c455703077a17a9b8d0fc655d939fcc6d24d819fa9a1066b74f710c35a43cbc8","68baea05aa0c3619b6feb78c80a07e27e4e68f921d714b8125f916c3b3370bf2","c13acdc7567b225971cef2416a3a2b03c8a4d8d154df48afe75834e2f5c59ddf","queue","5","5","5","5","5","5","2","2","2","2"]

    with open(file3path, mode='w', newline='') as file3:
        writer = csv.writer(file3)
        writer.writerow(header3)
        for _ in range(func_num):
            writer.writerow(row_data)

    print(f"Generated {file3path}")

    file4name = f"memory.csv"
    file4path = os.path.join(output_dir, file4name)

    header4 = ["HashOwner","HashApp","HashFunction","SampleCount","AverageAllocatedMb","AverageAllocatedMb_pct1","AverageAllocatedMb_pct5","AverageAllocatedMb_pct25","AverageAllocatedMb_pct50","AverageAllocatedMb_pct75","AverageAllocatedMb_pct95","AverageAllocatedMb_pct99","AverageAllocatedMb_pct100"]
    row_data = ["c455703077a17a9b8d0fc655d939fcc6d24d819fa9a1066b74f710c35a43cbc8","68baea05aa0c3619b6feb78c80a07e27e4e68f921d714b8125f916c3b3370bf2","c13acdc7567b225971cef2416a3a2b03c8a4d8d154df48afe75834e2f5c59ddf","19342.0","120.0","100.0","102.0","114.0","123.0","127.0","136.0","143.0","152.0"]

    with open(file4path, mode='w', newline='') as file4:
        writer = csv.writer(file4)
        writer.writerow(header4)
        for _ in range(func_num):
            writer.writerow(row_data)

    print(f"Generated {file4path}")

parser = argparse.ArgumentParser(description="Add two numbers.")
parser.add_argument('func_num', type=int)
parser.add_argument('serve_time', type=int)

args = parser.parse_args()
generate_csv_files(args.func_num, args.serve_time)