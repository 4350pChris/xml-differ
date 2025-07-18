// This file is auto-generated by @hey-api/openapi-ts

import type { Options as ClientOptions, TDataShape, Client } from "./client";
import type {
  GetLawsLawsGetData,
  GetLawsLawsGetResponses,
  GetLawsLawsGetErrors,
  GetLawLawsLawIdGetData,
  GetLawLawsLawIdGetResponses,
  GetLawLawsLawIdGetErrors,
  GetParagraphsVersionsVersionIdParagraphsGetData,
  GetParagraphsVersionsVersionIdParagraphsGetResponses,
  GetParagraphsVersionsVersionIdParagraphsGetErrors,
  GetDiffDiffLeftVersionIdRightVersionIdGetData,
  GetDiffDiffLeftVersionIdRightVersionIdGetResponses,
  GetDiffDiffLeftVersionIdRightVersionIdGetErrors,
  StartWorkImportPostData,
  StartWorkImportPostResponses,
} from "./types.gen";
import { client as _heyApiClient } from "./client.gen";

export type Options<TData extends TDataShape = TDataShape, ThrowOnError extends boolean = boolean> = ClientOptions<
  TData,
  ThrowOnError
> & {
  /**
   * You can provide a client instance returned by `createClient()` instead of
   * individual options. This might be also useful if you want to implement a
   * custom client.
   */
  client?: Client;
  /**
   * You can pass arbitrary values through the `meta` object. This can be
   * used to access values that aren't defined as part of the SDK function.
   */
  meta?: Record<string, unknown>;
};

/**
 * Get Laws
 */
export const getLawsLawsGet = <ThrowOnError extends boolean = false>(
  options?: Options<GetLawsLawsGetData, ThrowOnError>,
) => {
  return (options?.client ?? _heyApiClient).get<GetLawsLawsGetResponses, GetLawsLawsGetErrors, ThrowOnError>({
    url: "/laws",
    ...options,
  });
};

/**
 * Get Law
 */
export const getLawLawsLawIdGet = <ThrowOnError extends boolean = false>(
  options: Options<GetLawLawsLawIdGetData, ThrowOnError>,
) => {
  return (options.client ?? _heyApiClient).get<GetLawLawsLawIdGetResponses, GetLawLawsLawIdGetErrors, ThrowOnError>({
    url: "/laws/{law_id}",
    ...options,
  });
};

/**
 * Get Paragraphs
 */
export const getParagraphsVersionsVersionIdParagraphsGet = <ThrowOnError extends boolean = false>(
  options: Options<GetParagraphsVersionsVersionIdParagraphsGetData, ThrowOnError>,
) => {
  return (options.client ?? _heyApiClient).get<
    GetParagraphsVersionsVersionIdParagraphsGetResponses,
    GetParagraphsVersionsVersionIdParagraphsGetErrors,
    ThrowOnError
  >({
    url: "/versions/{version_id}/paragraphs/",
    ...options,
  });
};

/**
 * Get Diff
 */
export const getDiffDiffLeftVersionIdRightVersionIdGet = <ThrowOnError extends boolean = false>(
  options: Options<GetDiffDiffLeftVersionIdRightVersionIdGetData, ThrowOnError>,
) => {
  return (options.client ?? _heyApiClient).get<
    GetDiffDiffLeftVersionIdRightVersionIdGetResponses,
    GetDiffDiffLeftVersionIdRightVersionIdGetErrors,
    ThrowOnError
  >({
    url: "/diff/{left_version_id}/{right_version_id}",
    ...options,
  });
};

/**
 * Start Work
 */
export const startWorkImportPost = <ThrowOnError extends boolean = false>(
  options?: Options<StartWorkImportPostData, ThrowOnError>,
) => {
  return (options?.client ?? _heyApiClient).post<StartWorkImportPostResponses, unknown, ThrowOnError>({
    url: "/import",
    ...options,
  });
};
