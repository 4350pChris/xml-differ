import { apply } from "vike-server/h3";
import { serve } from "vike-server/h3/serve";
import installCrypto from "@hattip/polyfills/crypto";
import installGetSetCookie from "@hattip/polyfills/get-set-cookie";
import installWhatwgNodeFetch from "@hattip/polyfills/whatwg-node";
import { createApp } from "h3";

installWhatwgNodeFetch();
installGetSetCookie();
installCrypto();

const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 5173;

function startServer() {
  const app = createApp();
  apply(app);
  return serve(app, {
    port,
    hostname: "0.0.0.0",
  });
}

export default startServer();
