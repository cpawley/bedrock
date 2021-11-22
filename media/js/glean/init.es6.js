/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import Glean from '@mozilla/glean/web';

import {
    pageView as pageViewPing,
    click as clickPing
} from './generated/pings.js';
import * as pageMetrics from './generated/page.js';

Glean.setLogPings(true);
Glean.setDebugViewTag('moz-bedrock');
Glean.initialize('moz-bedrock', true);

pageMetrics.viewed.set();
pageMetrics.id.set(Mozilla.Analytics.getPageId(location.pathname));
pageViewPing.submit();

const buttons = document.querySelectorAll('.mzp-c-button[data-cta-text]');

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener(
        'click',
        (e) => {
            const id = e.target.getAttribute('data-cta-text');
            pageMetrics.element.set(id);
            clickPing.submit();
        },
        false
    );
}
