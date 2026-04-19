package game

import (
	"image"
	"image/color"
	"math"
	"os"

	"golang.org/x/image/draw"

	// Import PNG decoder so image.Decode handles PNG files.
	_ "image/png"
)

const imageSize = 64

// Image manages all game sprites loaded from disk.
// images[typeID] is a flat slice of frames; the state index directly selects
// the frame, matching the Python layout where each type-ID maps to a list of
// PIL images and state is used as the list index.
type Image struct {
	images [255][]image.Image
}

// NewImage loads all sprite sheets from the given base directory (the directory
// that contains the "imgs/" sub-folder).
func NewImage(baseDir string) (*Image, error) {
	img := &Image{}
	if err := img.addWall(baseDir); err != nil {
		return nil, err
	}
	if err := img.addItems(baseDir); err != nil {
		return nil, err
	}
	if err := img.addWeapons(baseDir); err != nil {
		return nil, err
	}
	if err := img.addEnemyGuard(baseDir); err != nil {
		return nil, err
	}
	if err := img.addEnemyDog(baseDir); err != nil {
		return nil, err
	}
	return img, nil
}

func loadPNG(path string) (image.Image, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	img, _, err := image.Decode(f)
	return img, err
}

func cropImage(src image.Image, x0, y0, x1, y1 int) image.Image {
	type subImager interface {
		SubImage(r image.Rectangle) image.Image
	}
	if si, ok := src.(subImager); ok {
		return si.SubImage(image.Rect(x0, y0, x1, y1))
	}
	// Fallback: copy pixels into a new NRGBA image.
	dst := image.NewNRGBA(image.Rect(0, 0, x1-x0, y1-y0))
	draw.Copy(dst, image.Point{}, src, image.Rect(x0, y0, x1, y1), draw.Src, nil)
	return dst
}

// addWall loads walls.png. Each wall type (0-54) stores two frames: index 0 is
// the horizontal-hit face, index 1 is the vertical-hit face — matching
// Python's images[i][0] and images[i][1].
func (im *Image) addWall(baseDir string) error {
	src, err := loadPNG(baseDir + "/imgs/walls.png")
	if err != nil {
		return err
	}
	for i := 0; i < 55; i++ {
		imgX := (i % 3) * 2 * imageSize
		imgY := int(math.Floor(float64(i)/3)) * imageSize
		im.images[i] = []image.Image{
			cropImage(src, imgX, imgY, imgX+imageSize, imgY+imageSize),
			cropImage(src, imgX+imageSize, imgY, imgX+imageSize*2, imgY+imageSize),
		}
	}
	return nil
}

// addItems loads items.png. Each item type has one frame at index 0.
func (im *Image) addItems(baseDir string) error {
	src, err := loadPNG(baseDir + "/imgs/items.png")
	if err != nil {
		return err
	}
	for i := 0; i < 64; i++ {
		imgX := i%5*imageSize + i%5
		imgY := int(math.Floor(float64(i)/5))*imageSize + int(math.Floor(float64(i)/5))
		im.images[56+i] = []image.Image{
			cropImage(src, imgX, imgY, imgX+imageSize, imgY+imageSize),
		}
	}
	return nil
}

// addWeapons loads weapons.png. Each weapon (types 120-123) stores 5 frames
// (states 0-4) for the idle and shooting animation steps.
func (im *Image) addWeapons(baseDir string) error {
	src, err := loadPNG(baseDir + "/imgs/weapons.png")
	if err != nil {
		return err
	}
	for i := 0; i < 4; i++ {
		imgY := i * imageSize
		frames := make([]image.Image, 5)
		for j := 0; j < 5; j++ {
			x1 := j + imageSize*j
			x2 := j + imageSize*(j+1)
			frames[j] = cropImage(src, x1, imgY, x2, imgY+imageSize)
		}
		im.images[120+i] = frames
	}
	return nil
}

// addEnemyGuard loads enemy-guard.png. Type 130 has 7×8 = 56 frames.
func (im *Image) addEnemyGuard(baseDir string) error {
	src, err := loadPNG(baseDir + "/imgs/enemy-guard.png")
	if err != nil {
		return err
	}
	var frames []image.Image
	for i := 0; i < 7; i++ {
		imgY := imageSize*i + i
		for j := 0; j < 8; j++ {
			imgX := imageSize*j + j
			frames = append(frames, cropImage(src, imgX, imgY, imgX+imageSize, imgY+imageSize))
		}
	}
	im.images[130] = frames
	return nil
}

// addEnemyDog loads enemy-dog.png. Type 131 has 7×8 = 56 frames.
func (im *Image) addEnemyDog(baseDir string) error {
	src, err := loadPNG(baseDir + "/imgs/enemy-dog.png")
	if err != nil {
		return err
	}
	var frames []image.Image
	for i := 0; i < 7; i++ {
		imgY := imageSize*i + i
		for j := 0; j < 8; j++ {
			imgX := imageSize*j + j
			frames = append(frames, cropImage(src, imgX, imgY, imgX+imageSize, imgY+imageSize))
		}
	}
	im.images[131] = frames
	return nil
}

// Get returns a sprite frame resized to (width × height).
// typeID selects the sprite slot; state is the frame index within that slot.
func (im *Image) Get(typeID, width, height, state int) image.Image {
	frames := im.images[typeID]
	var src image.Image
	if state < len(frames) {
		src = frames[state]
	}
	if src == nil {
		src = image.NewNRGBA(image.Rect(0, 0, imageSize, imageSize))
	}
	if width == imageSize && height == imageSize {
		return src
	}
	dst := image.NewNRGBA(image.Rect(0, 0, width, height))
	draw.ApproxBiLinear.Scale(dst, dst.Bounds(), src, src.Bounds(), draw.Src, nil)
	return dst
}

// GetColumn returns a single-pixel-wide column of a sprite, scaled to height.
// typeID and state select the sprite; col is the x offset within the sprite.
func (im *Image) GetColumn(typeID, col, height, state int) image.Image {
	frames := im.images[typeID]
	var src image.Image
	if state < len(frames) {
		src = frames[state]
	}
	if src == nil {
		src = image.NewNRGBA(image.Rect(0, 0, imageSize, imageSize))
	}
	colImg := cropImage(src, col, 0, col+1, imageSize)
	if height == imageSize {
		return colImg
	}
	dst := image.NewNRGBA(image.Rect(0, 0, 1, height))
	draw.NearestNeighbor.Scale(dst, dst.Bounds(), colImg, colImg.Bounds(), draw.Src, nil)
	return dst
}

// CreateBackground creates a background image split into dark top (sky) and
// light bottom (floor) halves, matching Python's Screen.create_background().
func CreateBackground(width, height int) *image.NRGBA {
	img := image.NewNRGBA(image.Rect(0, 0, width, height))
	half := height / 2
	sky := color.NRGBA{R: 30, G: 30, B: 30, A: 255}
	floor := color.NRGBA{R: 100, G: 100, B: 100, A: 255}
	for y := 0; y < height; y++ {
		c := floor
		if y < half {
			c = sky
		}
		for x := 0; x < width; x++ {
			img.SetNRGBA(x, y, c)
		}
	}
	return img
}
