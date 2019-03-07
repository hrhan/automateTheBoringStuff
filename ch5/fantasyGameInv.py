import time

def displayInventory(inventory):
	print("\nInventory:")
	total = 0
	for item, qty in inventory.items():
		print("{} {}".format(qty, item))
		total += qty
	print("Total number of items: {}\n".format(total))
	
def addToInventory(inventory, addedItems):
	for item in addedItems:
		print('+1 {}'.format(item))
		inventory[item] = inventory.setdefault(item, 0) + 1

if __name__ == '__main__':

	inv1 = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
	displayInventory(inv1)

	inv2 = {'gold coin': 42, 'rope': 1}
	dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
	addToInventory(inv2, dragonLoot)
	displayInventory(inv2)
