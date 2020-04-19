import globalAxios from 'axios';
import {UtilsApi} from '@/backend';

export const getLocalToken = () => localStorage.getItem('token');

export const saveLocalToken = (token: string) => localStorage.setItem('token', token);

export const removeLocalToken = () => localStorage.removeItem('token');

export const uploadImage = async (imageFile: File, token: string) => {
  const client = new UtilsApi({accessToken: token});
  const response = await client.getPresignedUrlApiV1UtilsGeturlPost(imageFile.type);

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
