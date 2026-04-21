package engine

import (
	"testing"
)

func TestAnimationInit(t *testing.T) {
	animateCalls := []float64{}
	animateEndCalled := 0

	onAnimate := func(f float64) { animateCalls = append(animateCalls, f) }
	onAnimateEnd := func() { animateEndCalled++ }

	anim := NewAnimation(2, onAnimate, onAnimateEnd)

	// initial state
	assertApprox(t, 2, anim.TotalTime(), "totalTime")
	assertApprox(t, 0, anim.Time(), "time")
	assertApprox(t, 0, anim.Factor(), "factor")
	if anim.IsAnimating() {
		t.Error("should not be animating initially")
	}

	anim.Start(0)
	assertApprox(t, 2, anim.TotalTime(), "totalTime after start")
	assertApprox(t, 0, anim.Time(), "time after start")
	assertApprox(t, 0, anim.Factor(), "factor after start (not updated yet)")
	if !anim.IsAnimating() {
		t.Error("should be animating after start")
	}

	anim.Update(0.5)
	assertApprox(t, 2, anim.TotalTime(), "totalTime 1")
	assertApprox(t, 0.5, anim.Time(), "time 1")
	assertApprox(t, 0.25, anim.Factor(), "factor 1")
	if !anim.IsAnimating() {
		t.Error("should still be animating")
	}
	if len(animateCalls) != 1 || animateCalls[0] != 0.25 {
		t.Errorf("onAnimate not called with 0.25, calls=%v", animateCalls)
	}
	if animateEndCalled != 0 {
		t.Error("onAnimateEnd should not have been called yet")
	}

	anim.Update(0.5)
	assertApprox(t, 2, anim.TotalTime(), "totalTime 2")
	assertApprox(t, 1, anim.Time(), "time 2")
	assertApprox(t, 0.5, anim.Factor(), "factor 2")
	if !anim.IsAnimating() {
		t.Error("should still be animating")
	}
	if animateCalls[len(animateCalls)-1] != 0.5 {
		t.Errorf("onAnimate last call should be 0.5, got %v", animateCalls)
	}
	if animateEndCalled != 0 {
		t.Error("onAnimateEnd should not have been called yet")
	}

	anim.Update(1)
	assertApprox(t, 2, anim.TotalTime(), "totalTime 3")
	assertApprox(t, 2, anim.Time(), "time 3")
	assertApprox(t, 1, anim.Factor(), "factor 3")
	if anim.IsAnimating() {
		t.Error("should have stopped animating")
	}
	if animateCalls[len(animateCalls)-1] != 1 {
		t.Errorf("onAnimate last call should be 1, got %v", animateCalls)
	}
	if animateEndCalled != 1 {
		t.Errorf("onAnimateEnd should have been called once, got %d", animateEndCalled)
	}
}
