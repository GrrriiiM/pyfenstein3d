package engine

// Decoration is a non-wall decorative sprite (may or may not be solid).
type Decoration struct {
	Item
}

// NewDecoration creates a new Decoration at the given position.
func NewDecoration(x, y float64, typeID int, isSolid bool) *Decoration {
	return &Decoration{Item: Item{block: newBlock(x, y, typeID, isSolid, false)}}
}
