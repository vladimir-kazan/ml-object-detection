import {
  Component,
  OnInit,
  AfterViewInit,
  ViewEncapsulation,
  ViewChild,
  ElementRef
} from '@angular/core';
// https://angular.io/guide/http
import { HttpClient, HttpRequest, HttpResponse, HttpEventType } from '@angular/common/http';

interface HTMLInputEvent extends Event {
  target: HTMLInputElement & EventTarget;
}

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class UploadComponent implements OnInit, AfterViewInit {

  public model = {
    file: '',
  }
  public image: any;
  public filename: string;

  @ViewChild("myCanvas") myCanvas: ElementRef;
  @ViewChild("myFile") myFile: ElementRef;

  private reader: FileReader;

  constructor(private http: HttpClient) {
    this.reader = new FileReader();
    this.reader.onload = this.onImageLoaded.bind(this);
    this.image = '';
    this.filename = 'Choose a file...';
  }

  ngOnInit() {}

  ngAfterViewInit() {}

  onFileChange(evt: HTMLInputEvent) {
    const files = evt.target.files;
    if (files && files[0]) {
      this.filename = files[0].name;
      this.reader.readAsDataURL(files[0]);

      // for canvas
      // const img = new Image;
      // img.src = URL.createObjectURL(files[0]);
      // img.onload = () => {
      //   const width = img.naturalWidth;
      //   const height = img.naturalHeight;
      //   const clientWidth = this.myCanvas.nativeElement.clientWidth; // 100%
      //   const ratioWidth = clientWidth / width;
      //   const clientHeight = height * ratioWidth;
      //   // fit to width
      //   let ctx = this.myCanvas.nativeElement.getContext('2d');
      //   ctx.scale(2, 2); // to increase quality, see also code below
      //   this.myCanvas.nativeElement.width = clientWidth * 2;
      //   this.myCanvas.nativeElement.height = clientHeight * 2;
      //   this.myCanvas.nativeElement.style.width = clientWidth + 'px';
      //   this.myCanvas.nativeElement.style.height = clientHeight + 'px';
      //   ctx.clearRect(0, 0, width, height);
      //   ctx.drawImage(img, 0, 0, width, height, 0, 0, clientWidth * 2, clientHeight * 2);
      // };
    }
  }

  private onImageLoaded() {
    this.image = this.reader.result;

    const formData = new FormData();
    formData.append('file', this.myFile.nativeElement.files[0]);
    const options = {
      reportProgress: true,
    };
    // TODO upload
    const req = new HttpRequest('POST', 'http://localhost:5000/upload', formData, options);

    this.http.request(req).subscribe(event => {
      // Via this API, you get access to the raw event stream.
      // Look for upload progress events.
      if (event.type === HttpEventType.UploadProgress) {
        // This is an upload progress event. Compute and show the % done:
        const percentDone = Math.round(100 * event.loaded / event.total);
        if (percentDone) {
          console.log(`File is ${percentDone}% uploaded.`);
        }
      } else if (event instanceof HttpResponse) {
        console.log('File is completely uploaded!');
      }
    }, error => {
      console.log('Error', error);
    });
  }
}
