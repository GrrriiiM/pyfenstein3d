package engine

import (
	"strconv"
	"strings"
)

// Map2d holds a parsed game map with all its entities.
type Map2d struct {
	grid    *ItemGrid
	players map[string]*Player
	persons []Blocker
	doors   []*Door
	enemies []*Enemy
}

// NewMap2d creates a Map2d from a list of blocks.
func NewMap2d(items []Blocker) *Map2d {
	m := &Map2d{
		grid:    NewItemGrid(items),
		players: make(map[string]*Player),
	}
	for _, item := range items {
		if p, ok := item.(*Player); ok {
			m.players[p.PlayerID()] = p
			m.persons = append(m.persons, item)
		}
		if d, ok := item.(*Door); ok {
			m.doors = append(m.doors, d)
		}
		if e, ok := item.(*Enemy); ok {
			m.enemies = append(m.enemies, e)
			m.persons = append(m.persons, item)
		}
	}
	return m
}

func (m *Map2d) Grid() *ItemGrid { return m.grid }

// Update advances all players and doors by deltaTime.
func (m *Map2d) Update(deltaTime float64) {
	for _, player := range m.players {
		player.Update(deltaTime, m.grid)
		player.AdjustCollision(m.grid)
		player.Cast(m.grid)
	}
	var persons []Blocker
	for _, player := range m.players {
		persons = append(persons, player)
	}
	for _, door := range m.doors {
		door.Update(deltaTime, persons)
	}
}

// GetPlayer returns the player with the given ID.
func (m *Map2d) GetPlayer(playerID string) *Player {
	return m.players[playerID]
}

// CreateWithPattern parses a hex pattern string and returns a Map2d.
func CreateWithPattern(pattern string) *Map2d {
	var items []Blocker
	lines := strings.Split(pattern, "\n")
	for blockY, line := range lines {
		for n := 0; n+1 < len(line); n += 2 {
			chunk := line[n : n+2]
			if strings.TrimSpace(chunk) == "" {
				continue
			}
			val, err := strconv.ParseInt(chunk, 16, 32)
			if err != nil {
				continue
			}
			typeID := int(val)
			blockX := n / 2
			bxf := float64(blockX)
			byf := float64(blockY)

			switch {
			case isWallSolid(typeID):
				items = append(items, NewWall(bxf, byf, typeID))
			case isWeapon(typeID):
				items = append(items, NewItemWeapon(bxf+0.5, byf+0.5, typeID))
			case isAmmo(typeID):
				items = append(items, NewItemAmmo(bxf+0.5, byf+0.5, typeID))
			case isScore(typeID):
				items = append(items, NewItemScore(bxf+0.5, byf+0.5, typeID))
			case isDecorationNonSolid(typeID):
				items = append(items, NewDecoration(bxf+0.5, byf+0.5, typeID, false))
			case isDecorationSolid(typeID):
				items = append(items, NewDecoration(bxf+0.5, byf+0.5, typeID, true))
			case isDoorHorizontal(typeID):
				items = append(items, NewDoor(bxf, byf+0.5, typeID, false))
			case isDoorVertical(typeID):
				items = append(items, NewDoor(bxf+0.5, byf, typeID, true))
			case isEnemy(typeID):
				items = append(items, CreateEnemy(bxf+0.5, byf+0.5, typeID))
			case isPlayerType(typeID):
				items = append(items, CreatePlayer(bxf+0.5, byf+0.5, typeID))
			}
		}
	}
	return NewMap2d(items)
}

var typeIDsDecorationsSolid = map[int]bool{
	57: true, 60: true, 61: true, 63: true, 65: true, 66: true, 68: true,
	69: true, 70: true, 71: true, 74: true, 75: true, 76: true, 80: true,
	93: true, 94: true, 95: true, 97: true,
}

func isWallSolid(id int) bool {
	return (id >= 0 && id < 48) || id == 53 || id == 54
}
func isWeapon(id int) bool             { return id == 85 || id == 86 }
func isAmmo(id int) bool               { return id == 84 }
func isScore(id int) bool              { return id == 87 || id == 88 || id == 89 }
func isDecorationSolid(id int) bool    { return typeIDsDecorationsSolid[id] }
func isDecorationNonSolid(id int) bool { return id >= 56 && id < 120 && !typeIDsDecorationsSolid[id] }
func isDoorHorizontal(id int) bool     { return id == 50 }
func isDoorVertical(id int) bool       { return id == 49 }
func isPlayerType(id int) bool         { return id == 255 }
func isEnemy(id int) bool              { return id == 130 || id == 131 }
