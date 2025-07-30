"""
Prompt generator for SQL query generation from natural language.

This module provides a function to create a prompt for an LLM to generate
PostgreSQL queries based on natural language input and database schema.
"""

def generate_sql_prompt(user_query: str, db_schema: str, include_examples: bool = True) -> str:
    """
    Generate a prompt for an LLM to convert natural language to SQL.
    
    Args:
        user_query: The natural language query from the user
        db_schema: A string containing the database schema summary
        include_examples: Whether to include example queries in the prompt
        
    Returns:
        A formatted prompt string for the LLM
    """
    # Base prompt with instructions
    prompt = f"""You are an expert PostgreSQL query generator. Your task is to convert natural language queries into correct and efficient PostgreSQL queries.

## Database Schema
Below is a summary of the database schema:

{db_schema}

## User Query
The user wants to: {user_query}

## Guidelines
- Use the exact table and column names as shown in the schema
- Include proper joins based on the relationships in the schema
- Use double quotes for table and column names that contain uppercase letters or are PostgreSQL keywords
- Keep the query as simple as possible while fulfilling the requirements
- Add comments to explain complex parts of the query
- Return only the SQL query without any additional explanation

"""

    # Add example queries if requested
    if include_examples:
        prompt += """
## Example Queries
Here are some example queries for reference:

### 1. Barrels currently available for sale
```sql
SELECT b.id, b."shortId", b.status, br.price, br."filledAt"
FROM public."barrel" b
JOIN public."barrelReference" br ON b."barrelRefrenceId" = br.id
WHERE br."quantityForSale" > 0 AND b.locked = FALSE;
```

### 2. Products with brand and cooperage details
```sql
SELECT p.id, p.status, b.name AS brand_name, c.name AS cooperage_name
FROM public."product" p
JOIN public."brand" b ON p."brandId" = b.id
JOIN public."cooperage" c ON p."cooperageId" = c.id;
```

### 3. Ownership history of a specific barrel
```sql
SELECT boh.*, o1.name AS sold_by, o2.name AS bought_by
FROM public."barrelOwnershipHistory" boh
LEFT JOIN public."organization" o1 ON boh."soldByOrganizationId" = o1.id
LEFT JOIN public."organization" o2 ON boh."buyByOrganizationId" = o2.id
WHERE boh."barrelId" = '<BARREL_UUID>';
```

### 4. Users in a specific organization and their roles
```sql
SELECT u.id, u.name, m.role, o.name AS organization_name
FROM public."user" u
JOIN public."member" m ON u.id = m."userId"
JOIN public."organization" o ON m."organizationId" = o.id
WHERE o.name = 'Your Organization Name';
```

### 5. Recent webhook events and their status
```sql
SELECT "event_type", "is_success", "created_at", error
FROM public."StraddleWebhookLog"
ORDER BY "created_at" DESC
LIMIT 10;
```

### 6. New fill products in the deal room
```sql
SELECT nfp.id, b.name AS brand_name, pt.name AS product_type
FROM public."newFillProduct" nfp
JOIN public."brand" b ON nfp."brand_id" = b.id
JOIN public."productType" pt ON nfp."product_type_id" = pt.id
WHERE nfp."is_in_deal_room" = TRUE;
```
"""

    # Final instruction
    prompt += """
## Output
Based on the user query and database schema, generate the appropriate PostgreSQL query:

```sql
"""

    return prompt
