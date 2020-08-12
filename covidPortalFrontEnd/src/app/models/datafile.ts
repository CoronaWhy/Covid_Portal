export class Datafile {
  name:string;
  chksum:string;
}

export class Log {
  processName:string;
  logValue:string;
}

export class UploadFolder {
  id:string;
  name:string;
  fileName:string;
  fileType:string;
  user:string;
  chksum:string;
  description:string;
  status:string;
  uploadedDate:Date;
  analysisProtocol:string;
  analysisSubmittedDate:Date;
  analysisCompletedDate:Date;
  rowColor:string;
  resultsAvailable:boolean;
  logs:Log;
}

export class UploadFolderSubmitObj {
  uploadFolder:UploadFolder;
  message:string;
}
