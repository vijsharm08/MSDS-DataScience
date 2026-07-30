# Image Generation Assignment - Complete Guide

## Overview
This guide will help you complete your generative AI image generation assignment, which has two main components:

1. **Image Comparison (6-8 images)**: Generate 3-4 images using the same prompts across 2 different AI platforms
2. **Jupyter Notebook**: Use Stable Diffusion API to generate and edit images with narrative

## Part 1: Generate Images Across Multiple Platforms

### Recommended Platforms (Choose 2)

#### Option 1: **DALL-E 3** (via ChatGPT Plus)
- **Access**: Requires ChatGPT Plus subscription ($20/month)
- **URL**: https://chat.openai.com/
- **How to use**: Simply paste your prompt and it generates images
- **Strengths**: Excellent prompt following, good with text in images
- **Cost**: $20/month subscription

#### Option 2: **Microsoft Copilot** (Free!)
- **Access**: Free with Microsoft account
- **URL**: https://copilot.microsoft.com/
- **How to use**: Click "Create" or use prompt like "Generate an image of..."
- **Strengths**: Free, powered by DALL-E 3, accessible
- **Cost**: FREE

#### Option 3: **Adobe Firefly** (Free tier available)
- **Access**: Free Adobe account
- **URL**: https://firefly.adobe.com/
- **How to use**: Use "Text to Image" feature
- **Strengths**: Commercial-safe, good quality, integrates with Adobe Creative Cloud
- **Cost**: Free tier available

#### Option 4: **Stable Diffusion** (via Replicate, DreamStudio, or local)
- **Access**: See the Jupyter Notebook I created
- **URL**: https://replicate.com/ or https://beta.dreamstudio.ai/
- **Strengths**: Open source, highly customizable
- **Cost**: Pay per generation (Replicate) or credits (DreamStudio)

#### Option 5: **Midjourney** (Requires Discord)
- **Access**: Discord account + subscription
- **URL**: https://www.midjourney.com/
- **How to use**: Use Discord bot with /imagine command
- **Strengths**: Artistic quality, beautiful aesthetics
- **Cost**: $10/month minimum

### The Four Prompts to Use

Use these exact prompts across both platforms:

1. **Landscape:** "A serene mountain lake at sunset, with snow-capped peaks reflected in crystal clear water, pine trees in the foreground, vibrant orange and purple sky, photorealistic, 8k quality"

2. **Character:** "A wise elderly wizard with a long silver beard, wearing deep blue robes embroidered with golden stars, holding a glowing staff, kind eyes, detailed fantasy art style, dramatic lighting"

3. **Abstract:** "Abstract representation of artificial intelligence: flowing neural networks made of light, geometric patterns, cyan and magenta color palette, digital art, futuristic, high contrast"

4. **Architectural:** "Modern sustainable architecture: glass and timber eco-house built into a hillside, large windows, green roof with plants, solar panels, minimalist design, architectural photography style"

### Steps for Part 1

1. **Choose your two platforms** (Recommendation: Microsoft Copilot + Adobe Firefly for free options)

2. **Generate images on Platform 1:**
   - Go to the platform
   - Submit all 4 prompts
   - Download each image and save with clear names (e.g., "landscape_copilot.png")

3. **Generate images on Platform 2:**
   - Repeat the process with the exact same prompts
   - Download and save (e.g., "landscape_firefly.png")

4. **Review your 6-8 images:**
   - You should now have 8 images (4 prompts × 2 platforms)
   - Or 6 images if you used 3 prompts

5. **Write your comparison paper:**
   - Use the provided template: `Image_Comparison_Paper_Template.md`
   - Insert your images
   - Write 250-500 words comparing similarities and differences
   - Save as Word document or PDF for submission

## Part 2: Jupyter Notebook with Stable Diffusion

### Option A: Use Replicate API (Recommended - Easiest)

1. **Get API Key:**
   - Go to https://replicate.com/
   - Sign up for a free account
   - Get your API token from https://replicate.com/account/api-tokens
   - First $0.01 worth of credits are free, then pay-as-you-go

2. **Open the Jupyter Notebook:**
   - Open `image_generation_assignment.ipynb` in VS Code or Jupyter

3. **Add your API key:**
   - Find the line: `os.environ["REPLICATE_API_TOKEN"] = "your-api-key-here"`
   - Replace with your actual API key

4. **Run all cells:**
   - Execute each cell in order
   - Wait for images to generate (30-60 seconds each)

5. **Add your observations:**
   - Fill in the markdown cells with your thoughts after each image generates

### Option B: Use DreamStudio (Stability AI Official)

1. **Get API Key:**
   - Go to https://beta.dreamstudio.ai/
   - Sign up (get free credits)
   - Get API key from account settings

2. **Modify the notebook:**
   - Replace the Replicate code with Stability AI SDK
   - Install: `pip install stability-sdk`
   - Use their documentation: https://platform.stability.ai/docs

### Option C: Run Locally (Advanced - Free but Complex)

1. **Requirements:**
   - NVIDIA GPU with 8GB+ VRAM
   - 20GB+ disk space
   - Python 3.10+

2. **Install:**
   ```bash
   pip install diffusers transformers accelerate torch
   ```

3. **Use Hugging Face:**
   - Get token from https://huggingface.co/settings/tokens
   - Download models from Hugging Face
   - Modify notebook to use local inference

### What to Include in Your Notebook

Your notebook should have:
1. ✅ **Markdown cells** explaining what you're doing
2. ✅ **Code cells** that generate images
3. ✅ **Generated images** displayed in the notebook
4. ✅ **Image editing example** (img2img)
5. ✅ **Narrative reflection** on:
   - How easy/hard the API was to use
   - Quality of results
   - Any surprises or challenges
   - Your overall thoughts

## Submission Checklist

### For Image Comparison Assignment:
- [ ] Generated 3-4 images on Platform 1
- [ ] Generated same 3-4 images on Platform 2
- [ ] Total of 6-8 images
- [ ] Written 250-500 word formal paper
- [ ] Paper follows APA format
- [ ] Images are embedded in the paper
- [ ] Comparisons discuss similarities AND differences
- [ ] References included

### For Jupyter Notebook Assignment:
- [ ] Jupyter notebook runs without errors
- [ ] API key is configured (or instructions provided)
- [ ] Images are successfully generated
- [ ] Image editing demonstrated
- [ ] Markdown explains each step
- [ ] Narrative reflection on API usability included
- [ ] Personal thoughts on results included

## Tips for Success

### Writing the Comparison Paper:
- Be specific: Don't just say "Platform A is better" - explain WHY and HOW
- Compare technical aspects: resolution, detail, color accuracy
- Compare prompt interpretation: Did they understand the prompt correctly?
- Discuss artistic style: photorealistic vs. artistic interpretation
- Note unexpected results or surprises
- Consider practical use cases for each platform

### Using the Jupyter Notebook:
- Start with small inference steps (20-30) for faster testing
- Experiment with guidance_scale (7-12 is typical)
- Use negative prompts to avoid unwanted elements
- Save intermediate results
- Take screenshots if code doesn't run (show effort)
- Document any errors and troubleshooting steps

### If You Run Into Issues:

**Can't afford paid APIs?**
- Use FREE options: Microsoft Copilot + Adobe Firefly
- Use free tiers: Replicate gives small free credit
- Run locally if you have a GPU

**Image Generation Fails?**
- Check API key is correct
- Verify internet connection
- Try simpler prompts first
- Check API service status
- Use screenshots and document the issue

**Don't understand the code?**
- Add comments explaining what you think each line does
- Research functions you don't understand
- Document your learning process in markdown cells
- Show effort even if results aren't perfect

## Example Timeline

**Day 1 (1-2 hours):**
- Set up accounts on your chosen platforms
- Generate all 6-8 images
- Save and organize images

**Day 2 (2-3 hours):**
- Write comparison paper
- Format with APA style
- Embed images
- Proofread

**Day 3 (2-3 hours):**
- Get Replicate API key
- Run Jupyter notebook
- Generate images via API
- Add observations

**Day 4 (1 hour):**
- Final review
- Add reflections to notebook
- Test that everything works
- Submit

## Resources

### APA Formatting:
- https://apastyle.apa.org/
- Use Purdue OWL for APA guidelines

### Prompt Engineering Tips:
- Be specific with style keywords
- Include quality terms (8k, photorealistic, detailed)
- Specify lighting and mood
- Mention art style or artist names (if desired)
- Use negative prompts to exclude unwanted elements

### Troubleshooting:
- Replicate documentation: https://replicate.com/docs
- Stability AI docs: https://platform.stability.ai/docs
- Stack Overflow for technical issues

Good luck with your assignment! 🎨🤖
