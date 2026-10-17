def draw_debug_trail(driver, points):
    """Draw the cursor trail and circle the final point."""
    driver.execute_script(
        """
        const pts = arguments[0];
        const frag = document.createDocumentFragment();

        for (const [x, y] of pts) {
            const d = document.createElement('div');
            d.style.cssText = 'position:absolute;width:4px;height:4px;background:red;'
                + 'border-radius:50%;z-index:100000;pointer-events:none;'
                + 'left:' + (x + window.scrollX - 2) + 'px;'
                + 'top:' + (y + window.scrollY - 2) + 'px';
            frag.appendChild(d);
        }

        if (pts.length > 0) {
            const [x, y] = pts[pts.length - 1];
            const circle = document.createElement('div');

            circle.style.cssText = 'position:absolute;width:20px;height:20px;'
                + 'border:2px solid red;border-radius:50%;'
                + 'box-sizing:border-box;z-index:100001;pointer-events:none;'
                + 'left:' + (x + window.scrollX - 10) + 'px;'
                + 'top:' + (y + window.scrollY - 10) + 'px';

            frag.appendChild(circle);
        }

        document.body.appendChild(frag);
        """,
        points,
    )
