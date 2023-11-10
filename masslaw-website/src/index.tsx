import React from 'react';
import { createRoot } from 'react-dom/client';

import {WebApp} from './application/web_app';

createRoot(document.getElementById('root')!).render(<WebApp/>);