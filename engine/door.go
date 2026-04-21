package engine

// Door is a block that can open and close.
type Door struct {
	block
	isVertical   bool
	isOpened     bool
	isOpening    bool
	isClosing    bool
	originalX    float64
	originalY    float64
	openAnim     *Animation
	waitAnim     *Animation
	closeAnim    *Animation
}

// NewDoor creates a new Door at the given position.
func NewDoor(x, y float64, typeID int, isVertical bool) *Door {
	d := &Door{
		block:      newBlock(x, y, typeID, true, false),
		isVertical: isVertical,
		originalX:  x,
		originalY:  y,
	}
	d.openAnim = NewAnimation(DoorOpenVelocity, d.onOpeningAnimate, d.onOpeningAnimateEnd)
	d.waitAnim = NewAnimation(DoorIntervalClose, nil, d.onWaitingAnimateEnd)
	d.closeAnim = NewAnimation(DoorOpenVelocity, d.onClosingAnimate, d.onClosingAnimateEnd)
	return d
}

func (d *Door) IsVertical() bool { return d.isVertical }

func (d *Door) onOpeningAnimate(factor float64) {
	var vx, vy float64
	if !d.isVertical {
		vx = factor
	} else {
		vy = factor
	}
	d.setXY(d.originalX-vx, d.originalY-vy)
}

func (d *Door) onOpeningAnimateEnd() {
	d.isOpening = false
	d.isOpened = true
	d.isSolid = false
	d.waitAnim.Start(0)
}

func (d *Door) onWaitingAnimateEnd() {
	d.doClose()
}

func (d *Door) onClosingAnimate(factor float64) {
	var vx, vy float64
	if !d.isVertical {
		vx = 1 - factor
	} else {
		vy = 1 - factor
	}
	d.setXY(d.originalX-vx, d.originalY-vy)
}

func (d *Door) onClosingAnimateEnd() {
	d.isClosing = false
	d.isOpened = false
}

func (d *Door) doOpen() {
	d.openAnim.Start(0)
}

func (d *Door) doClose() {
	d.isSolid = true
	d.closeAnim.Start(0)
}

func (d *Door) GetBounds(fovAng float64) []*Vector2d {
	var dx, dy float64
	if !d.isVertical {
		dx = 1
	} else {
		dy = 1
	}
	return []*Vector2d{
		d.pos,
		d.pos.Add(NewVector2d(dx, dy)),
	}
}

func (d *Door) IsInFov(pos *Vector2d, fovAng, fovDelta, dist float64) bool {
	return blockIsInFov(d.GetBounds(fovAng), pos, fovAng, fovDelta, dist)
}

// Update advances all door animations by deltaTime.
func (d *Door) Update(deltaTime float64, persons []Blocker) {
	d.openAnim.Update(deltaTime)
	d.waitAnim.Update(deltaTime)
	d.closeAnim.Update(deltaTime)
}

// Interacted toggles the door open/close when the player interacts.
func (d *Door) Interacted() {
	if !d.isOpening && !d.isClosing {
		if !d.isOpened {
			d.doOpen()
		}
	}
}
