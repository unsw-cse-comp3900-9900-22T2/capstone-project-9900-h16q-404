import React from 'react';
import { message, Input } from 'antd';

function fileToDataURL(setImage, file) {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function () {
    setImage(reader.result);
    console.log(reader.result);
  };
  reader.onerror = function (error) {
    message.warning(`Invalid image type. Please try again. Error: ${error}`);
  };
}

export const uploadImg = (setImage, string) => {
  return (
    <div>
      <h4>{string}</h4>
      <div id='upload-img' className='input-group'>
        <Input
          type='file'
          onChange={(e) => {
            const [file] = e.target.files;
            fileToDataURL(setImage, file);
          }}
        />
      </div>
    </div>
  );
};
