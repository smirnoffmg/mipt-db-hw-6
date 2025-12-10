WITH customer_revenue AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        c.wealth_segment,
        COALESCE(SUM(oi.item_list_price_at_sale * oi.quantity), 0) AS total_revenue
    FROM customer c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    WHERE c.wealth_segment IS NOT NULL
    GROUP BY c.customer_id, c.first_name, c.last_name, c.wealth_segment
),
ranked_customers AS (
    SELECT 
        first_name,
        last_name,
        wealth_segment,
        total_revenue,
        ROW_NUMBER() OVER (PARTITION BY wealth_segment ORDER BY total_revenue DESC) AS revenue_rank
    FROM customer_revenue
)
SELECT first_name, last_name, wealth_segment, total_revenue
FROM ranked_customers
WHERE revenue_rank <= 5
ORDER BY wealth_segment, revenue_rank;

