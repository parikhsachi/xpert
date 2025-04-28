import { z } from "zod";
import { zodResponseFormat } from "openai/helpers/zod";

// First, let's define our schema structure
const ReceiptItem = z.object({
    id: z.number(),
    name: z.string(),
    price: z.number(),
    quantity: z.number()
});

const ReceiptResponse = z.object({
    item_list: z.array(ReceiptItem),
    subtotal: z.number(),
    tax: z.number(),
    total: z.number()
});

export async function callOpenAi(body) {
    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
            },
            body: JSON.stringify({
                model: 'gpt-4-vision-preview', // Using vision model for image processing
                messages: [
                    {
                        role: 'user',
                        content: [
                            {
                                type: 'text',
                                text: "Extract the receipt information and return it in the specified JSON format. Include all items with their quantities and prices, along with the subtotal, tax, and total amount."
                            },
                            {
                                type: 'image_url',
                                image_url: {
                                    url: `data:image/jpeg;base64,${body.base64String}`,
                                },
                            },
                        ],
                    },
                ],
                response_format: zodResponseFormat(ReceiptResponse, "receipt"),
                max_tokens: 4000,
                temperature: 0.1 // Lower temperature for more consistent formatting
            }),
        });

        const data = await response.json();
        
        // The response will be automatically formatted according to our schema
        const receiptData = data.choices[0].message.parsed;
        
        // Add user and member information to the response
        const parsedJson = {
            ...receiptData,
            mainUser: { name: body.user.email },
            people: body.members
        };

        console.log('Processed receipt data:', parsedJson);
        return parsedJson;

    } catch (error) {
        console.error('Error processing receipt:', error);
        throw new Error('Failed to process receipt. Please try again.');
    }
}