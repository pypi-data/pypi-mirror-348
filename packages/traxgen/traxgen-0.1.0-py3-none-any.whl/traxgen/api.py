from typing import List, Dict, Any, Union
from .planner import TrajectoryPlanner
from .multi_agent import generate_multi_agent_trajectory
from .utils import split_trajectory_by_agent
from .visualizer import visualize_multi_agent_trajectory, visualize_given_graph
from .validator import validate_agent_sequence, validate_styles, validate_return_format, validate_visualize, validate_routine_format, validate_customer_data_fields, extract_variable_fields, extract_fields_from_conditionals, validate_customer_data_requirements
from .data_creation import generate_customer_profile

from .parser import parse_routine_to_planner
from collections.abc import Iterable
import json
import re
from collections import ChainMap



def build_trajectory_for_user(
    agent_sequence: List[str],
    customer_data: Dict[str, Any],
    routine_data: Dict[str, Dict],
    style: Union[str, List[str]] = "tool_only",
    visualize: bool = False,
    additional_data_sources: Dict[str, Dict[str, Any]] = None
) -> Union[List[Any], Dict[str, Any]]:
    """
    Public-facing function to generate trajectories.
    """
    # from .multi_agent import generate_multi_agent_trajectory #delayed import

    result = {}
    
    if len(agent_sequence) == 1:
        agent = agent_sequence[0]
        planner = parse_routine_to_planner(routine_data[agent], customer_data)
        trajectories = planner.generate_valid_trajectories()
        google = planner.get_google_trajectory(trajectories)

        for s in style:
            if s == "tool_only":
                result["tool_only"] = trajectories
            elif s == "google":
                result["google"] = google
            elif s == "langchain":
                result["langchain"] = planner.get_langchain_tool_trajectory(google)
            elif s == "our":
                result["our"] = planner.format_our_trajectory(trajectories)

        if visualize:
            for i, traj in enumerate(trajectories):
                visualize_given_graph(planner.build_graph_with_order(traj), filename=f"output/graph_{agent}_{i}.png")

    else:
        multi_agent_trajectories, planners = generate_multi_agent_trajectory(agent_sequence, customer_data, routine_data)

        for s in style:
            result[s] = []

        for i, traj in enumerate(multi_agent_trajectories):
            split = split_trajectory_by_agent(traj)
            if "tool_only" in style:
                result["tool_only"].append([tool for tools in split.values() for tool in tools])
            if "google" in style:
                result["google"].append(TrajectoryPlanner.format_google_multi_agent_trajectory(split, planners[i]))
            if "langchain" in style:
                result["langchain"].append(TrajectoryPlanner.format_langchain_multi_agent_trajectory(split, planners[i]))
            if "our" in style:
                result["our"].append(TrajectoryPlanner.format_our_multi_agent_trajectory(split, planners[i]))

            if visualize:
                visualize_multi_agent_trajectory(traj, filename=f"output/vis_trajectory_{'_'.join(agent_sequence)}_{i}.png")

    return result

    
def generate_trajectories(
    agent_sequence: List[str],
    customer_data: List[Dict[str, Any]],
    routine_data: Dict[str, Dict],
    style: Union[str, List[str]] = "tool_only",
    visualize: bool = False,
    return_format: str = "return",
    customer_data_path: str = '.',
    additional_data_sources: Dict[str, Dict[str, Any]] = None
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    
    validate_agent_sequence(agent_sequence, routine_data)
    validate_styles(style)
    validate_return_format(return_format, customer_data, customer_data_path)
    validate_visualize(visualize)
    validate_routine_format(routine_data)

    if isinstance(style, str):
        style = [style]
    
    results = {}

    # print('CUSTOMER DATA', type(customer_data))
    if type(customer_data) == dict: #there is only one customer
        customer_data = [customer_data]
    
    #decide to do customer data validation or not based on style (skip for tool only)
    validate_customer_data_requirements(routine_data, style, customer_data)
    

    if not customer_data:
        # print("No customer data provided. Generating default empty user.")
        customer_data = [{"customer_id": 0000}]  # fallback case
    
    for customer_profile in customer_data:
        # print('RPFIOLE EHRE:', customer_profile)
        customer_id = customer_profile.get("customer_id")
        # print(f"Generating trajectory for customer {customer_id}")

        result = build_trajectory_for_user(
            agent_sequence=agent_sequence,
            customer_data=customer_profile,
            routine_data=routine_data,
            style=style,
            visualize=visualize,
            # return_format="return", 
            # customer_data_path=customer_data_path
        )

        results[customer_id] = result

    if return_format == "trajectory_only":
        if not customer_data_path.endswith(".json"):
            customer_data_path = f"{customer_data_path}.json"
            
        with open(customer_data_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Saved ground truth for all customers to {customer_data_path}")
        return results

    if return_format == "data_and_trajectory":
        if not customer_data_path.endswith(".json"):
            customer_data_path = f"{customer_data_path}.json"

        # Map from customer_id to customer profile
        customer_map = {cust["customer_id"]: cust for cust in customer_data}
    
        for customer_id, trajectory in results.items():
            if customer_id in customer_map:
                customer_map[customer_id]["ground_truth_trajectories"] = trajectory
            else:
                print(f"Warning: Customer ID {customer_id} not found in original file.")
    
        with open(customer_data_path, "w") as f:
            json.dump(list(customer_map.values()), f, indent=2)
    
        print(f"Updated customer data with trajectories and saved to {customer_data_path}")
        # return list(customer_map.values())

    return results


def generate_trajectories_from_profiles(
    customer_data: List[Dict[str, Any]],
    routine_data: Dict[str, Dict],
    unique_identifier: str = 'customer_id',
    style: Union[str, List[str]] = "tool_only",
    visualize: bool = False,
    return_format: str = "return",
    customer_data_path: str = '.',
    additional_data_sources: Dict[str, Dict[str, Any]] = None
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    ### here, we assume that the client data has a field for agent sequence that can be different for different clients

    validate_styles(style)
    validate_visualize(visualize)
    validate_routine_format(routine_data)
    validate_return_format(return_format, customer_data, customer_data_path) 

    if isinstance(style, str):
        style = [style]

    results = {}

    if not customer_data:
        raise ValueError("Error: Customer data is needed for 'generate_trajectories_from_profiles'. 'generate_trajectories' sometimes allows no customer data.")

    validate_customer_data_requirements(routine_data, style, customer_data)
    
    if additional_data_sources:
        # one‐time, O(N) wrap, zero copying per‐profile
        customer_profiles = [
            ChainMap(profile, additional_data_sources)
            for profile in customer_data
        ]
    else:
        customer_profiles = customer_data

    for customer_profile in customer_profiles:
        # print(customer_profile)
        customer_id = customer_profile.get(unique_identifier)
        agent_sequence = customer_profile.get("agent_sequence")
        # print(agent_sequence)
        if type(agent_sequence) == str:
            agent_sequence = [agent_sequence]

        if not agent_sequence:
            raise ValueError(f"No agent_sequence found for customer {customer_id}")

        validate_agent_sequence(agent_sequence, routine_data)

        # print(f"Generating trajectory for customer {customer_id}")

        result = build_trajectory_for_user(
            agent_sequence=agent_sequence,
            customer_data=customer_profile,
            routine_data=routine_data,
            style=style,
            visualize=visualize,
            additional_data_sources = additional_data_sources
        )

        results[customer_id] = result

    if return_format == "trajectory_only":
        if not customer_data_path.endswith(".json"):
            customer_data_path = f"{customer_data_path}.json"
        with open(customer_data_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Saved ground truth for all customers to {customer_data_path}")
        return results

    if return_format == "data_and_trajectory":
        if not customer_data_path.endswith(".json"):
            customer_data_path = f"{customer_data_path}.json"

        for customer in customer_data:
            cid = customer[unique_identifier]
            if cid in results:
                customer["ground_truth_trajectories"] = results[cid]

        with open(customer_data_path, "w") as f:
            json.dump(customer_data, f, indent=2)
        print(f"Updated customer data with trajectories and saved to {customer_data_path}")

    return results


def get_required_fields(routine_data: dict) -> set:
    """Collect all required fields across multiple routines."""
    all_fields = set()
    all_fields.add('agent_sequence')
    for routine_name, routine in routine_data.items():
        # print('++++++++++ANALYZING ROUTINE', routine_name)
        # print(routine)
        steps = routine.get("steps", [])
        conditionals = routine.get("conditionals", [])
        if not isinstance(conditionals, list):
            conditionals = []
        fields = extract_variable_fields(steps) | extract_fields_from_conditionals(conditionals)
        all_fields |= fields

        # print('ALL FIELDS AT THIS ROUTINE', fields)

    if not all_fields:
        print('No specific customer data fields are needed for the routine(s) provided.')

    ###to ensure that agent sequence is always first
    others = list(all_fields - {'agent_sequence'})
    return ['agent_sequence'] + others


def create_user_data(
    required_fields: set,
    user_field_values: dict,
    n: int = 1,
    save_to_file: bool = False,
    file_path: str = None
) -> list[dict]:
    profiles = []

    # —— Special case: fixed counts for agent_sequence ——
    seq_dist = user_field_values.get("agent_sequence")
    if isinstance(seq_dist, dict) and seq_dist and all(isinstance(v, int) for v in seq_dist.values()):
        # ignore 'n' entirely, generate exactly sum(counts) profiles
        for seq, count in seq_dist.items():
            # normalize the key to a list:
            if isinstance(seq, tuple):
                seq_list = list(seq)
            elif isinstance(seq, str):
                seq_list = [seq]
            else:
                seq_list = list(seq)  # in case it was already a list

            # temporarily force generation of just that one sequence
            saved_seq_dist = user_field_values["agent_sequence"]
            user_field_values["agent_sequence"] = { tuple(seq_list): 1.0 }

            for _ in range(count):
                profiles.append(generate_customer_profile(required_fields, user_field_values))

            # restore original distribution
            user_field_values["agent_sequence"] = saved_seq_dist

    else:
        # —— regular probabilistic sampling ——
        for _ in range(n):
            profiles.append(generate_customer_profile(required_fields, user_field_values))


    # '_id' comes first, 'user_provided_info' comes last
    for profile in profiles:
        sorted_profile = {}
        
        # 1) agent_sequence
        if "agent_sequence" in profile:
            sorted_profile["agent_sequence"] = profile["agent_sequence"]
        
        # 2) _id keys
        id_keys = sorted(k for k in profile if k.endswith("_id"))
        for k in id_keys:
            sorted_profile[k] = profile[k]



        # 3) everything else except user_provided_info
        for k in sorted(profile):
            if k in id_keys or k in ("agent_sequence", "user_provided_info"):
                continue
            sorted_profile[k] = profile[k]

        # 4) user_provided_info last
        if "user_provided_info" in profile:
            sorted_profile["user_provided_info"] = profile["user_provided_info"]


        profile.clear()
        profile.update(sorted_profile)

    # print(len(profiles))
    # print("Generated Profiles:")
    # for profile in profiles:
    #     print(profile)
    
    if save_to_file:
        if file_path is None:
            file_path = "customer_data.json"
        
        try:
            with open(file_path, 'w') as file:
                json.dump(profiles, file, indent=2)
            print(f"Data saved successfully to {file_path}")
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")
    
    return profiles

    
def create_field_template(required_fields: set) -> dict:
    template = {}

    for field in required_fields:
        field_name = field

        if re.search(r"date", field, re.IGNORECASE):
            template[field_name] = {
                "random_date('2025-01-01', '2025-12-31')": 1.0
            }
        elif re.search(r"_id", field, re.IGNORECASE):
            template[field_name] = {
                "random_int(1000, 9999)": 1.0
            }
        elif re.search(r"amount|paid|price|total|cost", field, re.IGNORECASE):
            template[field_name] = {
                "random_float(10.0, 1000.0)": 1.0
            }
        elif re.search(r"number", field, re.IGNORECASE):
            template[field_name] = {
                "random_int(1, 50)": 1.0
            }
        elif re.search(r"preference|type|method|mode|status", field, re.IGNORECASE):
            template[field_name] = {
                "Option1": 0.5,
                "Option2": 0.5
            }
        else:
            #fallback
            template[field_name] = {
                "Option1": 0.5,
                "Option2": 0.3,
                "Option3": 0.2
            }

    return template