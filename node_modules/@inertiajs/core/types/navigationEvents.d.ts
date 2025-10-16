/**
 * Determine if this mouse event should be intercepted for navigation purposes.
 * Links with modifier keys or non-left clicks should not be intercepted.
 * Content editable elements and prevented events are ignored.
 */
export declare function shouldIntercept(event: Pick<MouseEvent, 'altKey' | 'ctrlKey' | 'defaultPrevented' | 'target' | 'currentTarget' | 'metaKey' | 'shiftKey' | 'button'>): boolean;
/**
 * Determine if this keyboard event should trigger a navigation request.
 * Enter triggers navigation for both links and buttons currently.
 * Space only triggers navigation for buttons specifically.
 */
export declare function shouldNavigate(event: Pick<KeyboardEvent, 'key' | 'currentTarget'>): boolean;
