select
  order_id,
  user_id,
  product_id,
  quantity,
  created_at,
  quantity as total_items
from {{ ref('stg_orders') }}
