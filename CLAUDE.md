# Medici - Autonomous WhatsApp Medical Store Agent

## Project Overview

An autonomous WhatsApp business agent for two medical stores in Durgapur. Uses a MoE (Mixture of Experts) architecture:
- **DeepSeek V4 Flash** - Main brain/router (1M token context window)
- **Gemma (Vision)** - OCR for prescription images
- **PDF Inventory** - Simple text-based inventory (no vector DB needed)

## Architecture

```
User Message (WhatsApp)
       │
       ▼
┌──────────────────┐
│  WhatsApp        │
│  Webhook          │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
 Text      Image
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│DeepSeek│ │ Gemma  │
│ V4     │ │ Vision │
│Flash   │ │   OCR  │
└────┬───┘ └────┬───┘
     │          │
     └────┬─────┘
          │
          ▼
   ┌──────────────┐
   │ 1mg Web      │
   │ Scraper Tool │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ PDF Inventory│
   │ Lookup       │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Response to  │
   │ WhatsApp     │
   └──────────────┘
```

## Tech Stack

- **Backend**: Python + FastAPI
- **LLM**: DeepSeek V4 Flash (via API)
- **Vision**: Gemma (via API) - OCR only
- **Inventory**: PDF file (parsed to text on boot)
- **Self-Learning**: skill.md file (RLHF memory)

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI server, webhook endpoints |
| `skill.md` | Agent's self-editing system prompt |
| `pdf_loader.py` | Parses inventory PDF to text |
| `deepseek_client.py` | DeepSeek API integration |
| `gemma_vision.py` | Gemma OCR for prescriptions |
| `one_mg_scraper.py` | Tata 1mg drug lookup tool |
| `.env` | API keys (not committed) |

## Environment Variables (to be provided)

```bash
DEEPSEEK_API_KEY=your_deepseek_key
GEMMA_API_KEY=your_gemma_key
WHATSAPP_VERIFY_TOKEN=your_verify_token
BOSS_FATHER_PHONE=your_father_number
```

## Phases

### Phase 1: Repo Initialization & Server Setup
- [x] Python + FastAPI project structure
- [ ] Git repo init & remote connect
- [ ] Webhook routing (placeholder - WhatsApp gateway TBD)

### Phase 2: PDF Inventory Loader
- [ ] Parse inventory PDF on server boot
- [ ] Store parsed text in memory

### Phase 3: skill.md RLHF Engine
- [ ] Create skill.md with starter template
- [ ] Background thread to update learnings after conversations

### Phase 4: Gemma Vision Pipeline
- [ ] Image webhook handling
- [ ] Gemma OCR integration

### Phase 5: DeepSeek Main Brain & Web Scraper
- [ ] DeepSeek API integration
- [ ] Intent routing (friends/professors/Boss detection)
- [ ] 1mg web scraper tool

## Important Notes

1. **WhatsApp Gateway**: User will provide details later - use placeholder webhook
2. **API Keys**: Will be provided by user - use env vars with clear placeholders
3. **Inventory PDF**: Placeholder PDF path - user to provide actual file
4. **Boss's Father Number**: Will be provided - use placeholder in skill.md
5. **Git Remote**: `https://github.com/avijitshil/medici.git`

## Coding Guidelines

- Use async/await for all API calls
- Keep secrets in `.env` - never commit
- Log all LLM interactions for debugging
- Commit after each phase as per plan
