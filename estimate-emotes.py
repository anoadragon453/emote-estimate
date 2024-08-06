import canonicaljson
import os
import json

EVENT_SIZE_LIMIT_BYTES = 65536

def get_size_of_extra_fed_fields(file_path: str) -> int:
    """
    Get the size in bytes of the extra fields added to an event when it is sent
    over federation.

    This is useful as the event size limit is actually applied to the event's
    federation format, which includes these extra fields.

    Args:
        file_path: The path to the file containing the extra federation fields.
    
    Returns:
        The number of bytes of the data, after canonicalising it.
    """
    with open (file_path, 'r', encoding='utf-8') as f:
        data = f.read()

    json_data = json.loads(data)

    canonical_json_bytes = canonicaljson.encode_canonical_json(json_data)

    return len(canonical_json_bytes)

def process_image_packs(dir_path: str, fed_fields_bytes: int) -> None:
    # Ensure the directory exists
    if not os.path.isdir(dir_path):
        print(f"Directory {dir_path} does not exist.")
        return
    
    bytes_per_emote = []
    max_emote_count = 0
    
    for filename in os.listdir(dir_path):
        if filename.endswith('.json'):
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()

            json_data = json.loads(data)
            
            # Calculate the number of bytes of the canonical representation
            # of the JSON
            num_bytes = len(canonicaljson.encode_canonical_json(json_data))

            # Add the number of bytes that federation fields take up
            num_bytes += fed_fields_bytes
            
            # Number of keys under content->images
            num_emotes = len(json_data.get('content', {}).get('images', {}).keys())

            max_emote_count = max(max_emote_count, num_emotes)
            
            # Avoid division by zero
            if num_emotes > 0:
                division_result = num_bytes / num_emotes
            else:
                division_result = float('inf')  # or handle the case properly if needed
            
            # Note down the bytes/emote ratio. We'll average them all at the end.
            bytes_per_emote.append(division_result)
            
            # Print results
            print(f"{filename}: Emotes: {num_emotes}, Bytes: {num_bytes}, Bytes / Emotes: {division_result:.2f}")
    
    # Calculate the average of the number of bytes per emote
    bytes_per_emote_avg = sum(bytes_per_emote) / len(bytes_per_emote)

    # Calculate the number of emotes you can stick in an event given the
    # event size limit.
    emotes_per_event = EVENT_SIZE_LIMIT_BYTES / bytes_per_emote_avg

    print(f"\nAverage bytes / emote: {bytes_per_emote_avg:.2f}")
    print(f"Max count in pack data: {max_emote_count}")
    print(f"Max emotes that can fit in {EVENT_SIZE_LIMIT_BYTES} bytes: {int(emotes_per_event)}")

if __name__ == "__main__":
    json_dir_path = "./json"

    fed_fields_bytes = get_size_of_extra_fed_fields("./extra_federation_fields.json")

    process_image_packs(json_dir_path, fed_fields_bytes)