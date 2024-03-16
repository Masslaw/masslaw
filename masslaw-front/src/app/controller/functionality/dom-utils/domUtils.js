export function getRelativeOffset(child, parent) {
    const childRect = child.getBoundingClientRect();
    const parentRect = parent.getBoundingClientRect();

    const xOffset = childRect.left - parentRect.left + parent.scrollLeft;
    const yOffset = childRect.top - parentRect.top + parent.scrollTop;

    return { x: xOffset, y: yOffset };
}

export async function smoothScroll(element, targetX, targetY, duration = 1000) {
    const startX = element.scrollLeft;
    const startY = element.scrollTop;
    let startTime = null;
    return new Promise((resolve) => {
        function animateScroll(currentTime) {
            if (startTime === null) startTime = currentTime;
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeInOutQuad = (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
            element.scrollLeft = startX + (targetX - startX) * easeInOutQuad(progress);
            element.scrollTop = startY + (targetY - startY) * easeInOutQuad(progress);
            if (progress < 1) {
                window.requestAnimationFrame(animateScroll);
                return;
            }
            resolve();
        }
        window.requestAnimationFrame(animateScroll);
    });
}

export async function centerChildInParent(child, parent, duration=1000) {
    if (!(parent instanceof HTMLElement) || !(child instanceof HTMLElement)) return;
    const offset = getRelativeOffset(child, parent);
    let scrollToTop = offset.y + child.clientHeight / 2 - parent.clientHeight / 2;
    let scrollToLeft = offset.x + child.clientWidth / 2 - parent.clientWidth / 2;
    await smoothScroll(parent, scrollToLeft, scrollToTop, duration);
}

export function isElemVisibleWithinScrollableParent(elem, scrollableParent) {
    const elemRect = elem.getBoundingClientRect();
    const parentRect = scrollableParent.getBoundingClientRect();
    const isVerticallyVisible = elemRect.top < parentRect.bottom && elemRect.bottom > parentRect.top;
    const isHorizontallyVisible = elemRect.left < parentRect.right && elemRect.right > parentRect.left;
    return isVerticallyVisible && isHorizontallyVisible;
}
