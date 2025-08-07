==================================================
         Darwin X Engine - Solo Stratum Miner
==================================================

This system gives a low-hash ASIC (e.g. Bitaxe Gamma) the best possible chance
of mining a Bitcoin block using entropy-based header evolution and strict 
Bitcoin consensus.

----------------------------
🔧 SYSTEM REQUIREMENTS
----------------------------
- Python 3.10+
- A local Bitcoin Core node (fully synced)
- Bitaxe ASIC miner connected via USB (Serial Mode)
- Internet connection for Discord Webhook (optional)

----------------------------
📁 PROJECT STRUCTURE
----------------------------
core/
  main.py               - Master thread orchestrator
  config.json           - System configuration

header/
  header_generator.py   - Builds new headers with mutated entropy
  merkle_calc.py        - Constructs valid merkle root

score/
  darwin_score.py       - Scores headers based on entropy and hash quality

pool/
  header_pool.py        - Keeps rolling Top-N Darwin-scored headers

asic/
  asic_interface.py     - Sends headers to ASIC via USB, waits for result

rpc/
  block_template.py     - Fetches and manages live block template from node
  rpc_interface.py      - Submits blocks via `submitblock`

utils/
  logger.py             - Timestamped console logging
  stats_tracker.py      - Tracks and prints mining stats
  webhook.py            - Discord alerts on block found

----------------------------
⚙️ HOW TO USE
----------------------------
1. Edit `core/config.json` with:
   - Your Bitcoin RPC credentials
   - Your Bitaxe COM port
   - Your Discord webhook
   - Your payout address

2. Make sure Bitcoin Core is running and synced.
   Use:
       bitcoin-cli getblockchaininfo

3. Plug in your Bitaxe ASIC (must support serial mode).

4. Launch mining:
       Double-click `launch.bat`  (or run `python core/main.py` manually)

5. Monitor live stats every 20 seconds in terminal.

----------------------------
📤 DISCORD NOTIFICATIONS
----------------------------
A Discord message will be sent automatically when a valid block is found.

----------------------------
💡 NOTES
----------------------------
- Only valid, consensus-legal headers are generated.
- System restarts header generation automatically on new Bitcoin block.
- All logic is modular and thread-safe.
- This is optimized for small-scale solo miners seeking real block wins.

==================================================
       GLHF – may the entropy be with you ⚡
==================================================
