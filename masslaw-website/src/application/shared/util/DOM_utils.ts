export function getRelativeOffset(child: HTMLElement, parent: HTMLElement) {
    let xOffset = 0;
    let yOffset = 0;

    let currentNode = child;
    while (currentNode !== parent) {
        if (!currentNode) return {x: 0, y: 0}
        xOffset += currentNode.offsetLeft;
        yOffset += currentNode.offsetTop;
        currentNode = currentNode.offsetParent as HTMLElement;
    }

    return {x: xOffset, y: yOffset};
}

export function smoothScroll(element: HTMLElement, targetX: number, targetY: number, duration = 1000) {
    const startX = element.scrollLeft;
    const startY = element.scrollTop;

    let startTime: number | null = null;

    function animateScroll(currentTime: number) {
        if (startTime === null) startTime = currentTime;

        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        const easeInOutQuad = (t: number) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;

        element.scrollLeft = startX + (targetX - startX) * easeInOutQuad(progress);
        element.scrollTop = startY + (targetY - startY) * easeInOutQuad(progress);

        if (progress < 1) window.requestAnimationFrame(animateScroll);
    }

    window.requestAnimationFrame(animateScroll);
}

export function centerChildInParent(child: HTMLElement, parent: HTMLElement) {
    if (!(parent instanceof HTMLElement) || !(child instanceof HTMLElement)) return;

    const offset = getRelativeOffset(child, parent);

    let scrollToTop = offset.y + child.clientHeight / 2 - parent.clientHeight / 2;
    let scrollToLeft = offset.x + child.clientWidth / 2 - parent.clientWidth / 2;

    smoothScroll(parent, scrollToLeft, scrollToTop, 1000);
}

export default {};
