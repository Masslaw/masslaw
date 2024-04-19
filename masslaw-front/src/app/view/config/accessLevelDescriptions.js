import {caseAccessLevels} from "../../config/caseConsts";


export const accessLevelDescriptions = {
    [caseAccessLevels.owner]: "Every case has an owner, and only one. The owner has the highest level of access to the case. They can perform any action on the case.",
    [caseAccessLevels.manager]: "Managers have an administrative access to the case. They are exposed to the entirety of the case and its content. They have the ability to perform any action below the owner of the case.",
    [caseAccessLevels.editor]: "Editors have the ability to make changes to the case. In the storage hierarchy configured as accessible by them, they can upload and make changes to any file or document.",
    [caseAccessLevels.reader]: "Readers can only view the content of the case. In the storage hierarchy configured as accessible by them, they can view and comment on any file or document.",
}
