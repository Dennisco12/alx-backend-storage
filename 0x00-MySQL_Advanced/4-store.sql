-- This creates a trigger that decreases the quantity of an item after adding a new order

CREATE TRIGGER decrease
AFTER INSERT
ON orders
FOR EACH ROW
	UPDATE items SET quantity = items.quantity - NEW.number WHERE name = NEW.item_name
