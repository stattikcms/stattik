import { library, dom } from "@fortawesome/fontawesome-svg-core";

import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { faGraphQL } from './graphql'

library.add(fas, far, fab, faGraphQL)
dom.watch();
