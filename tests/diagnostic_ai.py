import asyncio
import logging
import sys
import os
from pathlib import Path

# Add project root to sys.path to allow imports from 'bot'
# This ensures we can import from the bot package regardless of how the script is launched
root_path = Path(__file__).parent.parent.absolute()
sys.path.append(str(root_path))

from dotenv import load_dotenv
try:
    from bot.utils.get_decision import create_trading_agent, fetch_decision
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Ensure you are running from the project root: {root_path}")
    sys.exit(1)

# Configure logging to be very verbose to capture everything
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("AI_Diagnostic")

async def main():
    # Load environment variables from root and bot/.env
    load_dotenv()
    load_dotenv(root_path / "bot" / ".env")

    symbol = "BTCUSDT"
    iterations = 5  # Test 5 consecutive requests to check for rate limiting

    print(f"\n🚀 Starting AI Diagnostic Tool")
    print(f"Target Symbol: {symbol}")
    print(f"Iterations: {iterations}")
    print("-" * 50)

    success_count = 0

    for i in range(1, iterations + 1):
        print(f"\n--- Request #{i} ---")
        try:
            # Create a fresh agent for each request
            agent = create_trading_agent()
            model_id = agent.model_id
            print(f"Using Model: {model_id}")

            print("Fetching decision (this may take a minute, check logs below for tool calls)...")
            # This will call the function we just added logging to
            result_data = await fetch_decision(agent, symbol)

            if result_data and result_data[0] and result_data[0].strip():
                content, final_model = result_data
                print(f"✅ SUCCESS: Received valid response from {final_model} ({len(content)} characters)")
                success_count += 1
            else:
                print(f"❌ FAILED: Received None or empty response")

        except Exception as e:
            print(f"💥 CRITICAL ERROR: {e}")
            logger.exception("Unexpected exception during diagnostic request")

        # Small delay to prevent immediate hammering, but close enough to test rate limits
        await asyncio.sleep(2)

    print("\n" + "=" * 50)
    print(f"Diagnostic Complete: {success_count}/{iterations} successful")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDiagnostic interrupted by user.")
