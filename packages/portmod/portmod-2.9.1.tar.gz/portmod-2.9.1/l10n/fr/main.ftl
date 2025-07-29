## Help Message Strings

description = Gestionnaire de paquets CLI, conçu pour l'empaquetage des fichiers mods de jeux vidéo
merge-help = Installer ou supprimer des paquets
sync-help = Récupérer et mettre à jour les dépôt d'archives de paquets à distance
unmerge-help = Supprime le paquet donné sans vérifier les dépendances.
no-confirm-help = Ne demande pas de confirmation et sélectionne toujours plutôt l'option par défaut.

## Query messages


## Package phase messages


## Module messages


## Dependency messages


# TODO: There are a number of context strings that may eventually be passed to DepError
# which should be internationalized


## Download messages


## Config messages


## News messages


## Flags messages


## Use flag messages


## Conflicts UI Messages


## Select messages


## Profile messages


## Use flag configuration messages


## VFS messages


## Loader messages


## Use string messages


## Questions


## Argparse generic


## Pybuild Messages


## Mirror Messages


## Repo Messages


## Init Messages


## Destroy Messages


## Prefix messages


## Locking Messages


## Validate Messages

sync-repositories-help = Dépôts d'archives à synchroniser. Si omis, tous les référentiels dans repos.cfg seront synchronisés.
# Placeholder shown in parameter lists
archive-placeholder = ARCHIVE
# Placeholder shown in parameter lists
atom-placeholder = ATOM
# Placeholder shown in parameter lists
directory-placeholder = DIRECTORY
# Placeholder shown in parameter lists
set-placeholder = SET
# Placeholder shown in parameter lists
query-placeholder = QUERY
# Placeholder shown in parameter lists
number-placeholder = NUMBER
# $command (String) - Name of the command
invalid-cli-help =
    Les options de ligne de commande non valides ont été passées à `portmod`
     Commandes doivent avoir une sous-commande ou être `portmod --version`
auto-depclean-help =
    Supprime automatiquement les dépendances inutiles avant de terminer.
    Équivalent à l'exécution de `portmod <prefix> merge --depclean` après d'autres opérations.
oneshot-help = Ne modifiez pas l'ensemble des paquets globaux lors de l'installation ou de la suppression de paquets
depclean-help =
    Supprime les paquets et leurs dépendances. Les paquets dépendant
     des paquets donnés seront également supprimés. Si aucun argument n'est donné,
     ceci va supprimera les paquets dont les autres paquets n'ont pas besoin et qui ne
     sont pas dans le fichier global ou dans l'ensemble du système.
package-help =
    Paquets à installer. Peut-être soit un paquet `atom` ("category/name"), un ensemble ("@set_name") ou un chemin d'archive source ("path/to/archive.ext").
     Si un chemin d'archive est passé comme argument, portmod recherchera les archives correspondantes utilisées par les paquets qu'il connaît. Portmod ne peut pas installer à partir d'archives arbitraires.
# Help Message Strings
search-help = Recherche dans le dépôt des paquets dont le nom ou l'atome correspondent aux termes de recherche donnés
# Help Message Strings
search-query-help = Phrases de requête de recherche à comparer
# Help Message Strings
searchdesc-help = Considère également les descriptions lors de la recherche
# cfg-update messages
# $file (String) - The file being modified
apply-above-change-qn = Souhaitez-vous appliquer le changement ci-dessus à { $file } ?
# cfg-update messages
cfg-update-nothing-to-do = Aucun fichier ne nécessite une mise à jour
# cfg-update messages
update-file-prompt = Quel fichier souhaitez-vous mettre à jour ?
# Help Message Strings
version-help = Affiche le numéro de version de Portmod.
# Help Message Strings
merge-select-help =
        Ajoute les paquets spécifiés au world set (non utilisé. Ceci est l'option
    	par défaut si deselect n'est pas renseigné).
# Help Message Strings
info-repositories = Dépôts :
# Help Message Strings
module-update-help = Lance les mise à jour du module.
# Misc
pkg-messages = Message pour le paquet { $atom } :
# Help Message Strings
newuse-help = Cette option a été fusionnée dans --update et est à présent dépréciée.
# Help Message Strings
update-help =
    Met à jour les paquets vers la meilleure version disponible et exclut les paquets
    s'ils ne sont pas à jour.
