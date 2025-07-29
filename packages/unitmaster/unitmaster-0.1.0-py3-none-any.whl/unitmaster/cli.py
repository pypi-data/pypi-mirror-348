import argparse
import sys
from unitmaster.converter import convert, get_available_units, get_available_categories
from unitmaster.exceptions import UnitMasterError


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='UnitMaster: A versatile unit conversion tool.',
        epilog='Example: unitmaster 100 m ft'
    )
    
    parser.add_argument('value', type=float, help='The value to convert')
    parser.add_argument('from_unit', help='The unit to convert from')
    parser.add_argument('to_unit', help='The unit to convert to')
    parser.add_argument(
        '-c', '--category', 
        help='Specify the category of units (optional)'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List all available units or units in a specific category'
    )
    parser.add_argument(
        '--decimal-places',
        type=int,
        default=6,
        help='Number of decimal places in the result (default: 6)'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    args = parser.parse_args()
    
    # Handle listing units
    if args.list:
        if args.category:
            try:
                units = get_available_units(args.category)
                print(f"Units in category '{args.category}':")
                for unit in units:
                    print(f"  - {unit}")
            except UnitMasterError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            categories = get_available_categories()
            print("Available unit categories:")
            for category in categories:
                print(f"  - {category}")
            print("\nUse 'unitmaster -l -c CATEGORY' to list units in a specific category.")
        sys.exit(0)
    
    # Perform conversion
    try:
        result = convert(args.value, args.from_unit, args.to_unit, args.category)
        
        # Format the result
        if args.decimal_places == 0:
            formatted_result = str(int(result))
        else:
            formatted_result = f"{result:.{args.decimal_places}f}"
        
        # Print result with colors unless disabled
        if args.no_color:
            print(f"{args.value} {args.from_unit} = {formatted_result} {args.to_unit}")
        else:
            print(f"\033[1m{args.value} {args.from_unit}\033[0m = \033[92m{formatted_result} {args.to_unit}\033[0m")
        
    except UnitMasterError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()