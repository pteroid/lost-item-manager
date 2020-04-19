import * as backend from '@/backend';
import globalAxios from 'axios';

export const getLocalToken = () => localStorage.getItem('token');

export const saveLocalToken = (token: string) => localStorage.setItem('token', token);

export const removeLocalToken = () => localStorage.removeItem('token');

export const getimageUrl = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      resolve(reader.result as string);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};

export const uploadImage = async (imageFile: File, token: string) => {
  const client = new backend.UtilsApi({accessToken: token});
  const response = await client.getPresignedUrlApiV1UtilsGeturlPost(imageFile.type);
  if (!response.data) {
    return;
  }

  const uploadURL = response.data.msg;
  await globalAxios.put(uploadURL, imageFile,
      {
        headers: {'Content-Type': imageFile.type},
      },
  );

  return uploadURL.split('?')[0] as string;
};

export const getDateString = (date) =>
  date.getFullYear() + '-'
  + ('0' + (date.getMonth() + 1)).slice(-2) + '-'
  + ('0' + date.getDate()).slice(-2);
