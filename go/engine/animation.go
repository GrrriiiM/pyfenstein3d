package engine

// Animation drives a time-based animation with optional callbacks.
type Animation struct {
	totalTime    float64
	time         float64
	factor       float64
	isAnimating  bool
	onAnimate    func(float64)
	onAnimateEnd func()
}

// NewAnimation creates a new Animation with the given duration and optional callbacks.
func NewAnimation(totalTime float64, onAnimate func(float64), onAnimateEnd func()) *Animation {
	return &Animation{
		totalTime:    totalTime,
		onAnimate:    onAnimate,
		onAnimateEnd: onAnimateEnd,
	}
}

func (a *Animation) TotalTime() float64  { return a.totalTime }
func (a *Animation) Time() float64       { return a.time }
func (a *Animation) Factor() float64     { return a.factor }
func (a *Animation) IsAnimating() bool   { return a.isAnimating }

// Start begins the animation, optionally at a given time offset.
func (a *Animation) Start(at float64) {
	a.time = at
	a.isAnimating = true
}

// Update advances the animation by deltaTime seconds.
func (a *Animation) Update(deltaTime float64) {
	if a.isAnimating {
		a.time += deltaTime
		a.factor = a.time / a.totalTime
		if a.factor > 1 {
			a.factor = 1
		}
		if a.onAnimate != nil {
			a.onAnimate(a.factor)
		}
		if a.factor >= 1 {
			a.isAnimating = false
			if a.onAnimateEnd != nil {
				a.onAnimateEnd()
			}
		}
	} else {
		a.factor = 0
	}
}
