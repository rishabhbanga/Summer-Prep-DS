import os, argparse

NUM_FILES = 10  # No. of test files (hard coded)

# Input file reader
def read_file(fpath):
    if not os.path.exists(fpath):
        raise FileNotFoundError(f"File does not exist at path: {fpath}!")
    with open(fpath, "r") as f:
        content = f.read().splitlines()
    return content

# Input file data parser
def parse_data(data):
    num_lifeguards = int(data[0])
    shift_schedule_lst = [
        list(map(int, data[i].split())) for i in range(1, num_lifeguards + 1)
    ]
    return num_lifeguards, shift_schedule_lst

# File writer for saving output/result
def write_res_to_file(res, fpath):
    with open(fpath, "w") as f:
        f.write(str(res))

def calc_final_coverage(num_lifeguards, shift_schedule_lst):
    shift_schedule_lst.sort()  # Sort by shift starting times

    # Min non-overlapping contribution by a lifeguard
    min_contribution = get_min_contribution(shift_schedule_lst)
    total_coverage = calc_initial_coverage(num_lifeguards, shift_schedule_lst)

    # Adjusting for coverage contribution by the "mysterious" lifeguard
    final_coverage = total_coverage - max(min_contribution, 0)
    return final_coverage

def calc_initial_coverage(num_lifeguards, shift_schedule_lst):
    total_coverage = 0  # Accumulates total time (non-overlapping) coverage
    prev_start, prev_end = shift_schedule_lst[0]
    for i in range(1, len(shift_schedule_lst)):
        curr_start, curr_end = shift_schedule_lst[i]
        if curr_start < prev_end:
            prev_end = max(curr_end, prev_end)
        else:
            total_coverage += (prev_end - prev_start)
            prev_start, prev_end = curr_start, curr_end
        # Add in coverage upon reaching the last shift in the sorted schedule
        if i == len(shift_schedule_lst) - 1:
            total_coverage += (prev_end - prev_start)
    return total_coverage

def get_min_contribution(shift_schedule_lst):
    min_contribution = 1e9
    for i in range(len(shift_schedule_lst)):
        curr_start, curr_end = shift_schedule_lst[i]
        lower_bound = curr_start
        if i > 0:
            lower_bound = max(lower_bound, shift_schedule_lst[i - 1][1])
        upper_bound = curr_end
        if i < len(shift_schedule_lst) - 1:
            upper_bound = min(upper_bound, shift_schedule_lst[i + 1][0])

        coverage_contribution = upper_bound - lower_bound
        min_contribution = min(coverage_contribution, min_contribution)
    return min_contribution

# Main runner for running all tasks
def run_tasks(input_dir, output_dir):
    for idx in range(1, NUM_FILES + 1):
        ip_fpath = os.path.join(input_dir, f"{idx}.in")
        num_lifeguards, shift_schedule_lst = parse_data(read_file(ip_fpath))

        res = calc_final_coverage(num_lifeguards, shift_schedule_lst)

        out_fpath = os.path.join(output_dir, f"{idx}.out")
        write_res_to_file(res, out_fpath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_dir", type=str, default="",
        help="dir containing input files with the test cases"
    )
    parser.add_argument(
        "--output_dir", type=str, default="",
        help="dir for saving output files corresonding to the test cases"
    )
    args = parser.parse_args()

    dirs = [args.input_dir, args.output_dir]
    for i, dir_ in enumerate(dirs):
        # Default input dir is set as curr dir from which code is being run
        # Default output dir is set as input dir
        # If output dir does not exist, creates new with argument provided
        if not dir_:
            dirs[i] = os.getcwd() if i == 0 else dirs[0]
        elif not os.path.exists(dir_):
            os.mkdir(args.output_dir)
            print("Created directory with name "+args.output_dir)

    run_tasks(*dirs)