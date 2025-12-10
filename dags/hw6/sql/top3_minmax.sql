WITH customer_totals AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        COALESCE(SUM(oi.item_list_price_at_sale * oi.quantity), 0) AS total_amount
    FROM customer c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id, c.first_name, c.last_name
),
ranked AS (
    SELECT 
        first_name,
        last_name,
        total_amount,
        ROW_NUMBER() OVER (ORDER BY total_amount ASC) AS rank_min,
        ROW_NUMBER() OVER (ORDER BY total_amount DESC) AS rank_max
    FROM customer_totals
)
SELECT first_name, last_name, total_amount, 
       CASE WHEN rank_min <= 3 THEN 'TOP-3 MIN' ELSE 'TOP-3 MAX' END AS category
FROM ranked
WHERE rank_min <= 3 OR rank_max <= 3
ORDER BY total_amount;

